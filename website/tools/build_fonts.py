#!/usr/bin/env python3
"""Subset Noto Serif SC down to the characters this course actually uses.

Headings and the site brand are set in a Chinese serif face. Shipping the full
CJK font would cost ~22 MB, and loading it from a CDN would re-introduce the
network dependency the site deliberately removed, so this script builds a small
local subset instead (~0.5 MB for the whole weight axis).

The generated files under website/assets/fonts/ are committed, so the ordinary
`python website/build.py` needs neither fontTools nor network access. Re-run
this script only after adding course content with genuinely new characters:

    pip install fonttools brotli
    python website/tools/build_fonts.py

Font: Noto Serif SC, SIL Open Font License 1.1.
"""

import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Set

ROOT_DIR = Path(__file__).resolve().parent.parent
COURSE_DIR = ROOT_DIR.parent
FONT_DIR = ROOT_DIR / "assets" / "fonts"

SOURCE_URL = (
    "https://raw.githubusercontent.com/notofonts/noto-cjk/main/"
    "Serif/Variable/OTF/Subset/NotoSerifSC-VF.otf"
)
SOURCE_NAME = "NotoSerifSC-VF.otf"
OUTPUT_NAME = "NotoSerifSC-subset.woff2"

# Punctuation and symbols that appear in headings or UI chrome but may be
# missing from the scanned course text.
EXTRA_CHARS = (
    "，。、；：？！“”‘’（）《》【】〔〕—…·～｜"
    "×÷±≈≤≥≠→←↑↓°％‰∞√∑∫∂αβγδεθλμνπρσφωΔΩ"
    "①②③④⑤⑥⑦⑧⑨⑩"
)


def _keep(char: str) -> bool:
    """Drop control characters and glyphs that only waste subset space."""
    if not char.isprintable():
        return False
    return char not in ("　", "﻿")


def gather_charset() -> Set[str]:
    """Every character the course text may need in the serif face."""
    chars: Set[str] = set(chr(code) for code in range(0x20, 0x7F))
    chars |= set(EXTRA_CHARS)

    if not COURSE_DIR.exists():
        print("Warning: %s not found; subsetting ASCII only." % COURSE_DIR)
        return chars

    for readme in COURSE_DIR.rglob("README.md"):
        chars |= set(readme.read_text(encoding="utf-8", errors="ignore"))
    for notebook in COURSE_DIR.rglob("*.ipynb"):
        try:
            data = json.loads(notebook.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for cell in data.get("cells", []):
            if cell.get("cell_type") == "markdown":
                chars |= set("".join(cell.get("source", [])))
    return chars


def download_source(target: Path) -> Path:
    if target.exists() and target.stat().st_size > 1_000_000:
        print("Using cached source font: %s" % target)
        return target
    print("Downloading %s ..." % SOURCE_URL)
    with urllib.request.urlopen(SOURCE_URL, timeout=180) as response:  # noqa: S310
        target.write_bytes(response.read())
    print("Downloaded %.1f MB" % (target.stat().st_size / 1024 / 1024))
    return target


def write_css() -> Path:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    css_path = FONT_DIR / "fonts.css"
    css_path.write_text(
        "/* Noto Serif SC, SIL Open Font License 1.1.\n"
        "   Subset to the characters used by this course; regenerate with\n"
        "   python website/tools/build_fonts.py */\n"
        "@font-face {\n"
        '  font-family: "Noto Serif SC";\n'
        "  font-style: normal;\n"
        "  font-weight: 400 700;\n"
        "  font-display: swap;\n"
        '  src: url("%s") format("woff2");\n'
        "}\n" % OUTPUT_NAME,
        encoding="utf-8",
    )
    return css_path


def main() -> int:
    try:
        from fontTools import subset  # noqa: F401
        try:
            import brotli  # noqa: F401
        except ImportError:
            import brotlicffi  # noqa: F401
    except ImportError:
        print("Missing tooling. Install it with:  pip install fonttools brotli")
        return 1

    charset = "".join(sorted(c for c in gather_charset() if _keep(c)))
    print("Subsetting to %d characters" % len(charset))

    cache_dir = Path(tempfile.gettempdir()) / "ai4m-fonts"
    cache_dir.mkdir(parents=True, exist_ok=True)
    source = download_source(cache_dir / SOURCE_NAME)

    charset_file = cache_dir / "charset.txt"
    charset_file.write_text(charset, encoding="utf-8")

    FONT_DIR.mkdir(parents=True, exist_ok=True)
    output = FONT_DIR / OUTPUT_NAME
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fontTools.subset",
            str(source),
            "--text-file=%s" % charset_file,
            "--flavor=woff2",
            "--layout-features=*",
            "--output-file=%s" % output,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr[-2000:])
        return result.returncode

    css_path = write_css()
    print("Wrote %s (%.0f KB)" % (output, output.stat().st_size / 1024))
    print("Wrote %s" % css_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
