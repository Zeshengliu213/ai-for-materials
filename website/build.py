#!/usr/bin/env python3
"""Build the AI for Materials Science course website.

Scans the course repository root for modules, READMEs, Jupyter notebooks, solutions, datasets
and slide decks, and renders a self-contained static site into ./dist/.

Usage:
    python website/build.py

Dependencies: markdown-it-py and Pygments (see website/requirements.txt).
"""

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

REQUIRED = (
    ("markdown_it", "markdown-it-py"),
    ("pygments", "Pygments"),
)


def check_dependencies() -> None:
    missing = []
    for module_name, package_name in REQUIRED:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
    if missing:
        sys.exit(
            "Missing build dependencies: %s\n"
            "Install them with:  pip install -r website/requirements.txt"
            % ", ".join(missing)
        )


# Generated every run. dist/files/ and dist/slides/ are deliberately kept:
# their contents are content-addressed, so unchanged files survive untouched
# and collect_modules() prunes whatever is no longer referenced.
GENERATED = (
    "index.html",
    "exercises.html",
    "robots.txt",
    "sitemap.xml",
    "modules",
    "notebooks",
    "solutions",
    "assets",
)


def clear_generated(dist_dir: Path, clean: bool) -> None:
    if clean and dist_dir.exists():
        shutil.rmtree(dist_dir)
        return
    for name in GENERATED:
        target = dist_dir / name
        if target.is_dir():
            shutil.rmtree(target, ignore_errors=True)
        elif target.exists():
            target.unlink()


def build(clean: bool = False, base_url: str = "") -> None:
    check_dependencies()
    from builder import collect, config, pages

    if base_url:
        config.set_base_url(base_url)

    dist_dir = config.DIST_DIR
    clear_generated(dist_dir, clean)
    dist_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        config.ASSETS_SRC,
        dist_dir / "assets",
        ignore=shutil.ignore_patterns(
            ".ruff_cache", "__pycache__", ".DS_Store", "*.map", "*.py"
        ),
    )

    modules = collect.collect_modules(dist_dir)
    pages.write_site(modules, dist_dir)

    # GitHub Pages 在「从分支部署」模式下会跑 Jekyll，而 Jekyll 默认跳过
    # 以下划线开头的路径 —— 那正是数据集去重目录 files/_shared/ 的名字。
    # 一个空的 .nojekyll 即可关掉这套处理，对 Actions 部署无副作用。
    (dist_dir / ".nojekyll").write_text("", encoding="utf-8")

    total_nbs = sum(len(m.notebooks) for m in modules)
    total_sols = sum(len(m.solutions) for m in modules)
    total_slides = sum(len(m.slides) for m in modules)
    total_exercises = sum(len(m.exercises) for m in modules)
    print(
        "Build complete: %d modules, %d notebooks (%d exercise), %d solutions, "
        "%d slide decks -> %s"
        % (len(modules), total_nbs, total_exercises, total_sols, total_slides, dist_dir)
    )
    if not config.SITE_BASE_URL:
        print(
            "Note: no public base URL set, so sitemap.xml, canonical links and "
            "Open Graph preview cards are skipped. Pass --base-url https://... "
            "or set AI4M_BASE_URL to enable them."
        )
    if not config.GITHUB_REPO:
        print(
            "Note: GITHUB_REPO is empty in website/builder/config.py, "
            "so the one-click 'Open in Colab' buttons are disabled."
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the course website into website/dist/.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="delete dist/ entirely first, instead of reusing copied datasets",
    )
    parser.add_argument(
        "--base-url",
        default="",
        metavar="URL",
        help="public site URL (e.g. https://user.github.io/repo) used for "
             "sitemap.xml, canonical links and social preview cards",
    )
    args = parser.parse_args()
    build(clean=args.clean, base_url=args.base_url)


if __name__ == "__main__":
    main()
