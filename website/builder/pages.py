"""Write every HTML page, the search index, the sitemap and robots.txt.

All markup lives in website/templates/; this module only prepares the context
each template needs.
"""

import json
from pathlib import Path
from typing import Dict, List

from markupsafe import Markup

from . import collect, config, notebooks, rendering, templating
from .collect import Module, PageRef


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _page_title(*parts: str) -> str:
    return " | ".join(part for part in parts if part)


# ---------------------------------------------------------------------------
# Notebook and solution pages
# ---------------------------------------------------------------------------


def write_notebook_pages(modules: List[Module], order: List[PageRef], dist_dir: Path) -> None:
    prefix = "../../"
    for module in modules:
        file_prefix = "%sfiles/%s/" % (prefix, module.slug)

        for nb in module.notebooks:
            href = "notebooks/%s/%s.html" % (module.slug, nb.stem)
            previous, following = collect.find_neighbours(order, href)
            cells, headings = notebooks.render_cells(nb.data, file_prefix)
            _write(
                dist_dir / href,
                templating.render(
                    "notebook.html",
                    p=prefix,
                    page_title=_page_title(nb.title, config.SITE_TITLE),
                    description=nb.search_text[:160] or config.SITE_DESCRIPTION,
                    modules=modules,
                    module=module,
                    nb=nb,
                    nb_solution=module.solution_for(nb),
                    canonical=config.page_url(href),
                    cells=Markup(cells),
                    headings=headings,
                    with_toc=True,
                    current_slug=module.slug,
                    current_nb=nb.stem,
                    previous=previous,
                    following=following,
                ),
            )

        for solution in module.solutions:
            href = "solutions/%s/%s.html" % (module.slug, solution.stem)
            cells, headings = notebooks.render_cells(solution.data, file_prefix)
            _write(
                dist_dir / href,
                templating.render(
                    "solution.html",
                    p=prefix,
                    page_title=_page_title("参考答案：%s" % solution.title, config.SITE_TITLE),
                    description="练习参考答案与解析。",
                    modules=modules,
                    module=module,
                    solution=solution,
                    canonical=config.page_url(href),
                    cells=Markup(cells),
                    headings=headings,
                    with_toc=True,
                    current_slug=module.slug,
                ),
            )


# ---------------------------------------------------------------------------
# Module pages
# ---------------------------------------------------------------------------


def write_module_pages(modules: List[Module], order: List[PageRef], dist_dir: Path) -> None:
    prefix = "../"
    for module in modules:
        href = "modules/%s.html" % module.slug
        previous, following = collect.find_neighbours(order, href)
        readme_html = ""
        if module.readme_md:
            readme_html = rendering.render_markdown(
                module.readme_md, "%sfiles/%s/" % (prefix, module.slug)
            )
        _write(
            dist_dir / href,
            templating.render(
                "module.html",
                p=prefix,
                page_title=_page_title(
                    "模块 %s：%s" % (module.num, module.zh_title), config.SITE_TITLE
                ),
                description=module.summary or config.SITE_DESCRIPTION,
                modules=modules,
                module=module,
                readme=Markup(readme_html) if readme_html else "",
                canonical=config.page_url(href),
                current_slug=module.slug,
                previous=previous,
                following=following,
            ),
        )


# ---------------------------------------------------------------------------
# Exercise hub page
# ---------------------------------------------------------------------------


def _progress_keys(modules: List[Module]) -> List[str]:
    """Every notebook page that counts towards the study-progress meter."""
    return [
        "notebooks/%s/%s.html" % (module.slug, nb.stem)
        for module in modules
        for nb in module.notebooks
    ]


def write_exercises_page(modules: List[Module], dist_dir: Path) -> None:
    """A single hub that collects every exercise notebook across all modules."""
    groups = []
    for module in modules:
        if not module.exercises and module.status == "todo":
            groups.append({"module": module, "rows": [], "planned": True})
            continue
        if not module.exercises:
            groups.append({"module": module, "rows": [], "planned": False})
            continue
        rows = []
        for nb in module.exercises:
            solution = module.solution_for(nb)
            rows.append(
                {
                    "nb": nb,
                    "href": "notebooks/%s/%s.html" % (module.slug, nb.stem),
                    "solution_href": (
                        "solutions/%s/%s.html" % (module.slug, solution.stem)
                        if solution
                        else ""
                    ),
                }
            )
        groups.append({"module": module, "rows": rows, "planned": False})

    total = sum(len(group["rows"]) for group in groups)
    _write(
        dist_dir / "exercises.html",
        templating.render(
            "exercises.html",
            p="",
            active="exercises",
            page_title=_page_title("全部习题与参考答案", config.SITE_TITLE),
            description="课程全部模块的习题 Notebook 与参考答案汇总，支持按模块查看完成进度。",
            modules=modules,
            groups=groups,
            total_exercises=total,
            progress_keys=",".join(
                row["href"] for group in groups for row in group["rows"]
            ),
            canonical=config.page_url("exercises.html"),
        ),
    )


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------


def _course_jsonld(modules: List[Module]) -> str:
    """Schema.org Course markup so search engines understand the syllabus."""
    payload: Dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": config.SITE_TITLE,
        "description": config.SITE_DESCRIPTION,
        "inLanguage": "zh-CN",
        "teaches": [module.zh_title for module in modules],
        "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online"},
    }
    if config.SITE_BASE_URL:
        payload["url"] = config.SITE_BASE_URL
    return json.dumps(payload, ensure_ascii=False)


def _colab_intro() -> Markup:
    if config.GITHUB_REPO:
        return Markup(
            "每份课件页面都有“在 Colab 中打开”按钮，点击即可在浏览器中直接运行，无需本地安装。"
        )
    return Markup(
        "下载任意模块的 <code>.ipynb</code> 课件并上传至 "
        '<a href="https://colab.research.google.com/" target="_blank" rel="noopener">'
        "Google Colab</a> 即可在浏览器中直接运行"
        "（课件内置了缺失依赖自动检测与数据上传引导）。"
    )


def _roadmap(modules: List[Module]) -> List[Dict[str, object]]:
    """Resolve ROADMAP_STAGES into real Module objects for the home page."""
    by_num = {module.num: module for module in modules}
    stages: List[Dict[str, object]] = []
    for index, stage in enumerate(config.ROADMAP_STAGES, start=1):
        members = [by_num[num] for num in stage["modules"] if num in by_num]
        if not members:
            continue
        stages.append(
            {
                "index": index,
                "icon": stage["icon"],
                "title": stage["title"],
                "desc": stage["desc"],
                "members": members,
                "done": all(m.status == "done" for m in members),
            }
        )
    return stages


def write_index_page(modules: List[Module], dist_dir: Path) -> None:
    _write(
        dist_dir / "index.html",
        templating.render(
            "index.html",
            p="",
            active="home",
            page_title=_page_title(config.SITE_TITLE, "材料人工智能实战课程"),
            modules=modules,
            part1=[m for m in modules if m.semester == "part1"],
            part2=[m for m in modules if m.semester == "part2"],
            total_notebooks=sum(len(m.notebooks) for m in modules),
            total_exercises=sum(len(m.exercises) for m in modules),
            all_progress_keys=",".join(_progress_keys(modules)),
            slide_modules=[m for m in modules if m.slides],
            roadmap=_roadmap(modules),
            canonical=config.page_url("index.html"),
            first_href="modules/%s.html" % modules[0].slug if modules else "#syllabus",
            colab_text=_colab_intro(),
            course_jsonld=Markup(_course_jsonld(modules)),
        ),
    )


# ---------------------------------------------------------------------------
# Search index, sitemap, robots
# ---------------------------------------------------------------------------


def _search_entry(title: str, href: str, kind: str, module_num: str, text: str) -> dict:
    return {"title": title, "href": href, "kind": kind, "module": module_num, "text": text}


def write_search_index(modules: List[Module], dist_dir: Path) -> None:
    entries: List[dict] = []
    for module in modules:
        entries.append(
            _search_entry(
                "模块 %s：%s" % (module.num, module.zh_title),
                "modules/%s.html" % module.slug,
                "module",
                module.num,
                rendering.plain_text(
                    "%s %s %s" % (module.summary, module.en_title, module.readme_md), 900
                ),
            )
        )
        for nb in module.notebooks:
            entries.append(
                _search_entry(
                    nb.title,
                    "notebooks/%s/%s.html" % (module.slug, nb.stem),
                    nb.kind if nb.is_exercise else "notebook",
                    module.num,
                    "%s %s" % (nb.filename, nb.search_text),
                )
            )
        for sol in module.solutions:
            entries.append(
                _search_entry(
                    "参考答案：%s" % sol.title,
                    "solutions/%s/%s.html" % (module.slug, sol.stem),
                    "solution",
                    module.num,
                    "%s %s" % (sol.filename, sol.search_text),
                )
            )

    # Emitted as JavaScript rather than JSON: fetch() of a local .json file is
    # blocked by CORS under file://, and the site must work when opened offline.
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    _write(
        dist_dir / "assets" / "search-index.js",
        "window.AI4M_SEARCH_INDEX = %s;\n" % payload,
    )


def write_sitemap(modules: List[Module], dist_dir: Path) -> None:
    if not config.SITE_BASE_URL:
        _write(dist_dir / "robots.txt", "User-agent: *\nAllow: /\n")
        return
    base = config.SITE_BASE_URL.rstrip("/")
    hrefs = ["index.html", "exercises.html"]
    hrefs += [ref.href for ref in collect.reading_order(modules)]
    hrefs += [
        "solutions/%s/%s.html" % (module.slug, sol.stem)
        for module in modules
        for sol in module.solutions
    ]
    urls = "".join("  <url><loc>%s/%s</loc></url>\n" % (base, href) for href in hrefs)
    _write(
        dist_dir / "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls,
    )
    _write(dist_dir / "robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % base)


def write_site(modules: List[Module], dist_dir: Path) -> None:
    _write(dist_dir / "assets" / "pygments.css", rendering.pygments_css())
    order = collect.reading_order(modules)
    write_index_page(modules, dist_dir)
    write_module_pages(modules, order, dist_dir)
    write_exercises_page(modules, dist_dir)
    write_notebook_pages(modules, order, dist_dir)
    write_search_index(modules, dist_dir)
    write_sitemap(modules, dist_dir)
