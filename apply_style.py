#!/usr/bin/env python3
"""把课程统一绘图风格（ai4m.mplstyle）注入到所有用 matplotlib 的 Notebook。

与 configure_colab.py 一样是**幂等**的：重复运行只会刷新已注入的格，不会越加越多。

    python apply_style.py              # 预演：只列出会改哪些文件
    python apply_style.py --write      # 真正写入
    python apply_style.py --write --include-solutions

注意：注入后 Notebook 里**已保存的旧图**仍是旧风格，需要重跑一遍单元格
（Kernel → Restart & Run All）才会变成新风格。
"""

import argparse
import json
import pathlib
from typing import List

COURSE_DIR = pathlib.Path(__file__).resolve().parent
MARKER = "# ai4m-style"
MD_MARKER = "<!-- ai4m-style -->"

MD_SOURCE: List[str] = [
    MD_MARKER + "\n",
    "> **📘 课程统一绘图风格**：下面这格加载课程自带的 `ai4m.mplstyle`"
    "（配色与课程网站同源，无上右边框，仅横向浅网格，保存默认 300 dpi）。"
    "`C` 是课程配色，手动指定颜色时写 `color=C.crimson`。\n",
]

CODE_SOURCE: List[str] = [
    MARKER + "：课程统一绘图风格（本地与 Colab 通用）\n",
    "import pathlib, sys\n",
    "\n",
    "sys.path.insert(0, str(pathlib.Path.cwd().parent))   # course/ 根目录\n",
    "import ai4m_style as ai4m\n",
    "\n",
    "C = ai4m.use()        # 应用 ai4m.mplstyle，返回课程配色\n",
]


def notebooks(include_solutions: bool) -> List[pathlib.Path]:
    found = []
    for path in sorted(COURSE_DIR.rglob("*.ipynb")):
        parts = path.parts
        if ".ipynb_checkpoints" in parts:
            continue
        if not include_solutions and "solutions" in parts:
            continue
        found.append(path)
    return found


def uses_matplotlib(data: dict) -> bool:
    code = "\n".join(
        "".join(c.get("source", []))
        for c in data.get("cells", [])
        if c.get("cell_type") == "code"
    )
    return "matplotlib" in code or "import seaborn" in code


def inject(path: pathlib.Path, write: bool) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not uses_matplotlib(data):
        return "skip (no matplotlib)"

    cells = [
        c for c in data.get("cells", [])
        if MARKER not in "".join(c.get("source", []))
        and MD_MARKER not in "".join(c.get("source", []))
    ]
    had = len(cells) != len(data.get("cells", []))

    anchor = None
    for index, cell in enumerate(cells):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and (
            "import matplotlib" in source or "import seaborn" in source
        ):
            anchor = index + 1
            break
    if anchor is None:  # 没有显式 import 的 Notebook：放在 colab-setup 之后
        anchor = next(
            (i + 1 for i, c in enumerate(cells) if "# colab-setup" in "".join(c.get("source", []))),
            1,
        )

    md_cell = {"cell_type": "markdown", "metadata": {}, "source": MD_SOURCE}
    code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": CODE_SOURCE,
    }
    cells[anchor:anchor] = [md_cell, code_cell]
    data["cells"] = cells

    if write:
        # newline="" 很关键：默认文本模式会把换行写成 CRLF，
        # 让每个 .ipynb 在 git 里显示成整文件改动。
        with path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    return ("refresh" if had else "inject") + " @ cell %d" % anchor


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="真正写入文件（默认只预演）")
    parser.add_argument("--include-solutions", action="store_true", help="同时处理 solutions/")
    args = parser.parse_args()

    changed = 0
    for path in notebooks(args.include_solutions):
        result = inject(path, args.write)
        if result.startswith("skip"):
            continue
        changed += 1
        print("%-60s %s" % (path.relative_to(COURSE_DIR).as_posix(), result))

    print("\n%d 个 Notebook %s。" % (changed, "已更新" if args.write else "将被更新（预演模式）"))
    if not args.write:
        print("确认无误后运行：python apply_style.py --write")
    else:
        print("提示：已保存的旧图仍是旧风格，重跑 Notebook 才会刷新。")


if __name__ == "__main__":
    main()
