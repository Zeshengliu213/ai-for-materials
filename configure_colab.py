"""
为 course/ 下所有 .ipynb 自动配置 Google Colab 一键打开徽章与云端环境初始化格。

用法（发布到 GitHub 前运行一次即可）：
    python configure_colab.py <你的GitHub用户名> <仓库名>

例如：
    python configure_colab.py zhangsan ai-for-materials
"""

import json
import pathlib
import re
import sys
import urllib.parse

COURSE_DIR = pathlib.Path(__file__).resolve().parent
DEFAULT_USER = "YOUR_GITHUB_USER"
DEFAULT_REPO = "ai-for-materials"

EXTRA_PKGS = ("rdkit", "xgboost", "selfies", "chemprop", "pymatgen")


def detect_extra_packages(nb_data: dict) -> list[str]:
    code = "\n".join(
        "".join(c.get("source", []))
        for c in nb_data.get("cells", [])
        if c.get("cell_type") == "code" and "# colab-setup" not in "".join(c.get("source", []))
    )
    needed = []
    for pkg in EXTRA_PKGS:
        if re.search(rf"(?:import|from)\s+{pkg}\b", code):
            needed.append(pkg)
    return needed


def make_badge_cell(user: str, repo: str, rel_posix: str) -> dict:
    encoded_path = urllib.parse.quote(rel_posix)
    colab_url = f"https://colab.research.google.com/github/{user}/{repo}/blob/main/{encoded_path}"
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "<!-- colab-badge -->\n",
            f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})",
        ],
    }


def make_setup_cell(user: str, repo: str, rel_dir_posix: str, extra_pkgs: list[str]) -> dict:
    lines = [
        "# colab-setup (本地运行时自动跳过)\n",
        "import os, sys\n",
        "\n",
        'if "google.colab" in sys.modules:\n',
        f'    _repo_dir = "/content/{repo}"\n',
        "    if not os.path.exists(_repo_dir):\n",
        f'        os.system("git clone --depth 1 https://github.com/{user}/{repo}.git " + _repo_dir)\n',
    ]
    if rel_dir_posix and rel_dir_posix != ".":
        lines.append(f'    os.chdir(os.path.join(_repo_dir, "{rel_dir_posix}"))\n')
    else:
        lines.append("    os.chdir(_repo_dir)\n")

    if extra_pkgs:
        pkg_str = " ".join(extra_pkgs)
        lines.append(f'    get_ipython().run_line_magic("pip", "install -q {pkg_str}")\n')

    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines,
    }


def update_notebook(nb_path: pathlib.Path, user: str, repo: str) -> None:
    nb_data = json.loads(nb_path.read_text(encoding="utf-8"))
    rel_posix = nb_path.relative_to(COURSE_DIR).as_posix()
    rel_dir_posix = nb_path.parent.relative_to(COURSE_DIR).as_posix()

    cells = nb_data.get("cells", [])

    # 移除旧的自动注入格（幂等更新）
    cleaned = []
    for c in cells:
        src = "".join(c.get("source", []))
        if "<!-- colab-badge -->" in src or "# colab-setup" in src:
            continue
        cleaned.append(c)

    extra_pkgs = detect_extra_packages(nb_data)
    badge_cell = make_badge_cell(user, repo, rel_posix)
    setup_cell = make_setup_cell(user, repo, rel_dir_posix, extra_pkgs)

    # 放在第 0 格（徽章）和第 1 格或标题后（初始化）
    if cleaned and cleaned[0].get("cell_type") == "markdown":
        new_cells = [badge_cell, cleaned[0], setup_cell] + cleaned[1:]
    else:
        new_cells = [badge_cell, setup_cell] + cleaned

    nb_data["cells"] = new_cells
    nb_path.write_text(json.dumps(nb_data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def update_readme(user: str, repo: str) -> None:
    readme_path = COURSE_DIR / "README.md"
    text = readme_path.read_text(encoding="utf-8")

    marker = "## ☁️ 在线运行（Google Colab）"
    if marker in text:
        text = text.split(marker)[0].rstrip() + "\n\n"
    else:
        text = text.rstrip() + "\n\n"

    notebooks = sorted(
        p for p in COURSE_DIR.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in p.parts and "solutions" not in p.parts
    )

    lines = [
        marker,
        "",
        "零基础同学无需在本地安装 Python，点击下方任意章节的 **Open in Colab** 徽章即可直接在浏览器运行：",
        "",
        "| 章节 | Notebook | 在线运行 |",
        "| :--- | :--- | :--- |",
    ]
    for nb in notebooks:
        rel = nb.relative_to(COURSE_DIR).as_posix()
        encoded = urllib.parse.quote(rel)
        url = f"https://colab.research.google.com/github/{user}/{repo}/blob/main/{encoded}"
        badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"
        lines.append(f"| `{nb.parent.name}` | `{nb.name}` | {badge} |")

    lines.extend([
        "",
        "> **教师发布提示**：上传到 GitHub 前，在 `course/` 目录执行 `python configure_colab.py <你的GitHub用户名> <仓库名>` 即可一键更新所有链接。",
        "",
    ])

    readme_path.write_text(text + "\n".join(lines), encoding="utf-8")


def main() -> None:
    user = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USER
    repo = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_REPO

    nbs = sorted(
        p for p in COURSE_DIR.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in p.parts
    )
    for nb in nbs:
        update_notebook(nb, user, repo)
    update_readme(user, repo)
    print(f"Updated {len(nbs)} notebooks and README.md for GitHub repo: {user}/{repo}")


if __name__ == "__main__":
    main()
