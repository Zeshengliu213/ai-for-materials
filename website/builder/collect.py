"""Scan the course/ folder and copy downloadable assets into dist/.

Dataset files are content-addressed: identical files (the 2.2 MB AqSolDB CSV is
reused by seven modules) are copied once into dist/files/_shared/ and linked
from every module that needs them.
"""

import hashlib
import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from . import config, notebooks

IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".svg", ".gif")
EXTRA_SUFFIXES = IMAGE_SUFFIXES + (".txt",)


def slugify(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return "%d B" % size_bytes
    if size_bytes < 1024 * 1024:
        return "%.1f KB" % (size_bytes / 1024)
    return "%.1f MB" % (size_bytes / (1024 * 1024))


@dataclass(frozen=True)
class Dataset:
    """A downloadable dataset, stored once in the shared content-addressed pool."""

    filename: str
    href: str          # relative to dist/ root
    size_label: str
    size_bytes: int


@dataclass(frozen=True)
class SlideDeck:
    """An HTML slide deck that accompanies a lecture."""

    name: str
    title: str
    href: str          # relative to dist/ root


EXERCISE_MARKER = "exercise"


def is_exercise_stem(stem: str) -> bool:
    """Exercise notebooks are named *_exercises.ipynb (01e_exercises, 02d_exercises...)."""
    return EXERCISE_MARKER in stem.lower()


@dataclass
class NotebookDoc:
    filename: str
    stem: str
    title: str
    data: dict
    size_label: str
    search_text: str
    download_href: str
    colab_url: str = ""

    @property
    def is_exercise(self) -> bool:
        return is_exercise_stem(self.stem)

    @property
    def kind(self) -> str:
        return "exercise" if self.is_exercise else "lecture"


@dataclass
class Module:
    num: str
    dir_name: str
    slug: str
    zh_title: str
    en_title: str
    semester: str
    status: str
    status_label: str
    summary: str
    outline: List[str] = field(default_factory=list)
    readme_md: str = ""
    notebooks: List[NotebookDoc] = field(default_factory=list)
    solutions: List[NotebookDoc] = field(default_factory=list)
    datasets: List[Dataset] = field(default_factory=list)
    slides: List[SlideDeck] = field(default_factory=list)

    @property
    def lectures(self) -> List[NotebookDoc]:
        return [nb for nb in self.notebooks if not nb.is_exercise]

    @property
    def exercises(self) -> List[NotebookDoc]:
        return [nb for nb in self.notebooks if nb.is_exercise]

    @property
    def lecture_solutions(self) -> List[NotebookDoc]:
        return [sol for sol in self.solutions if not sol.is_exercise]

    @property
    def exercise_solutions(self) -> List[NotebookDoc]:
        return [sol for sol in self.solutions if sol.is_exercise]

    def solution_for(self, nb: NotebookDoc) -> Optional[NotebookDoc]:
        """The solutions notebook that answers a given notebook, if any."""
        pool = self.exercise_solutions if nb.is_exercise else self.lecture_solutions
        return pool[0] if pool else None


class SharedFileStore:
    """Copy files into dist/files/_shared/<hash>-<name>, skipping duplicates."""

    def __init__(self, dist_dir: Path) -> None:
        self._dir = dist_dir / "files" / config.SHARED_FILES_DIRNAME
        self._dir.mkdir(parents=True, exist_ok=True)
        self._seen: Dict[str, str] = {}
        self.used_names: Set[str] = set()
        self.bytes_saved = 0
        self.bytes_reused = 0

    @staticmethod
    def _digest(path: Path) -> str:
        sha = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                sha.update(chunk)
        return sha.hexdigest()

    def add(self, source: Path) -> str:
        """Return the dist-relative href for a file, copying it only once."""
        digest = self._digest(source)
        key = "%s:%s" % (digest, source.name)
        if key in self._seen:
            self.bytes_saved += source.stat().st_size
            return self._seen[key]

        stored_name = "%s-%s" % (digest[:12], source.name)
        target = self._dir / stored_name
        # The name carries the content hash, so an existing file with this name
        # is already the right bytes and survives rebuilds untouched.
        if target.exists():
            self.bytes_reused += source.stat().st_size
        else:
            shutil.copy2(source, target)

        self.used_names.add(stored_name)
        href = "files/%s/%s" % (config.SHARED_FILES_DIRNAME, stored_name)
        self._seen[key] = href
        return href

    def prune(self) -> int:
        """Delete shared files left over from content that no longer exists."""
        removed = 0
        for item in self._dir.iterdir():
            if item.is_file() and item.name not in self.used_names:
                item.unlink()
                removed += 1
        return removed


def _load_notebook(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _collect_notebooks(
    paths: List[Path], store: SharedFileStore, module_dir_name: str, sub_path: str = ""
) -> List[NotebookDoc]:
    docs: List[NotebookDoc] = []
    for path in paths:
        data = _load_notebook(path)
        rel = "%s%s" % (sub_path, path.name)
        docs.append(
            NotebookDoc(
                filename=path.name,
                stem=path.stem,
                title=notebooks.extract_notebook_title(data, path.stem),
                data=data,
                size_label=format_size(path.stat().st_size),
                search_text=notebooks.notebook_search_text(data),
                download_href=store.add(path),
                colab_url=config.colab_url(module_dir_name, rel),
            )
        )
    return docs


def _collect_datasets(data_dir: Path, store: SharedFileStore) -> List[Dataset]:
    datasets: List[Dataset] = []
    if not data_dir.exists():
        return datasets
    for item in sorted(data_dir.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        size = item.stat().st_size
        datasets.append(
            Dataset(
                filename=item.name,
                href=store.add(item),
                size_label=format_size(size),
                size_bytes=size,
            )
        )
    return datasets


def _copy_module_images(module_dir: Path, files_dest: Path) -> None:
    """Images stay per-module: README Markdown links to them by relative path."""
    files_dest.mkdir(parents=True, exist_ok=True)
    for item in module_dir.iterdir():
        if item.is_file() and item.suffix.lower() in EXTRA_SUFFIXES:
            shutil.copy2(item, files_dest / item.name)
    img_dir = module_dir / "img"
    if img_dir.exists():
        shutil.copytree(img_dir, files_dest / "img", dirs_exist_ok=True)


def _slide_title(index_html: Path, fallback: str) -> str:
    try:
        text = index_html.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return fallback
    match = re.search(r"<title>(.*?)</title>", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else fallback


def _collect_slides(dist_dir: Path) -> Dict[str, List[SlideDeck]]:
    """Scan course/slides/<name>/index.html; <name> starts with the module number."""
    by_module: Dict[str, List[SlideDeck]] = {}
    if not config.SLIDES_DIR.exists():
        return by_module
    for deck_dir in sorted(config.SLIDES_DIR.iterdir()):
        index_html = deck_dir / "index.html"
        if not deck_dir.is_dir() or not index_html.exists():
            continue
        match = re.match(r"^(\d{2})", deck_dir.name)
        if not match:
            continue
        shutil.copytree(deck_dir, dist_dir / "slides" / deck_dir.name, dirs_exist_ok=True)
        by_module.setdefault(match.group(1), []).append(
            SlideDeck(
                name=deck_dir.name,
                title=_slide_title(index_html, "讲课幻灯片 %s" % deck_dir.name),
                href="slides/%s/index.html" % deck_dir.name,
            )
        )
    return by_module


def collect_modules(dist_dir: Path) -> List[Module]:
    if not config.COURSE_DIR.exists():
        raise FileNotFoundError("Course directory not found: %s" % config.COURSE_DIR)

    store = SharedFileStore(dist_dir)
    slides_by_module = _collect_slides(dist_dir)
    modules: List[Module] = []

    for entry in sorted(config.COURSE_DIR.iterdir(), key=lambda p: p.name):
        if not entry.is_dir():
            continue
        match = re.match(r"^(\d{2})\s*-\s*(.+)$", entry.name)
        if not match:
            continue
        num, raw_name = match.group(1), match.group(2).strip()
        slug = slugify(entry.name)
        meta = config.module_meta(num, raw_name)

        _copy_module_images(entry, dist_dir / "files" / slug)

        sol_dir = entry / "solutions"
        readme_path = entry / "README.md"
        sol_paths = sorted(sol_dir.glob("*.ipynb")) if sol_dir.exists() else []

        modules.append(
            Module(
                num=num,
                dir_name=entry.name,
                slug=slug,
                zh_title=str(meta["zh_title"]),
                en_title=str(meta["en_title"]),
                semester=str(meta["semester"]),
                status=str(meta["status"]),
                status_label=str(meta["status_label"]),
                summary=str(meta["summary"]),
                outline=list(meta.get("outline") or []),
                readme_md=readme_path.read_text(encoding="utf-8") if readme_path.exists() else "",
                notebooks=_collect_notebooks(sorted(entry.glob("*.ipynb")), store, entry.name),
                solutions=_collect_notebooks(sol_paths, store, entry.name, "solutions/"),
                datasets=_collect_datasets(entry / "data", store),
                slides=slides_by_module.get(num, []),
            )
        )

    _prune_stale_dirs(dist_dir / "files", {m.slug for m in modules} | {config.SHARED_FILES_DIRNAME})
    _prune_stale_dirs(
        dist_dir / "slides",
        {deck.name for decks in slides_by_module.values() for deck in decks},
    )
    removed = store.prune()

    print("Shared-file de-duplication saved %s" % format_size(store.bytes_saved))
    if store.bytes_reused:
        print("Reused %s of unchanged files from the previous build" % format_size(store.bytes_reused))
    if removed:
        print("Pruned %d stale shared file(s)" % removed)
    return modules


def _prune_stale_dirs(parent: Path, keep: Set[str]) -> None:
    """Remove generated subdirectories whose source content is gone."""
    if not parent.exists():
        return
    for item in parent.iterdir():
        if item.is_dir() and item.name not in keep:
            shutil.rmtree(item, ignore_errors=True)


@dataclass(frozen=True)
class PageRef:
    """One entry in the linear reading order, used for prev/next navigation."""

    title: str
    href: str          # relative to dist/ root
    module_num: str


def reading_order(modules: List[Module]) -> List[PageRef]:
    order: List[PageRef] = []
    for module in modules:
        order.append(
            PageRef(
                title="模块 %s · %s" % (module.num, module.zh_title),
                href="modules/%s.html" % module.slug,
                module_num=module.num,
            )
        )
        for nb in module.notebooks:
            order.append(
                PageRef(
                    title=nb.title,
                    href="notebooks/%s/%s.html" % (module.slug, nb.stem),
                    module_num=module.num,
                )
            )
    return order


def find_neighbours(
    order: List[PageRef], href: str
) -> Tuple[Optional[PageRef], Optional[PageRef]]:
    """Return (previous, next) entries around a page; either may be None."""
    for index, ref in enumerate(order):
        if ref.href != href:
            continue
        previous = order[index - 1] if index > 0 else None
        following = order[index + 1] if index + 1 < len(order) else None
        return previous, following
    return None, None
