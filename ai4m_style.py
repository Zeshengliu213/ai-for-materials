"""AI for Materials Science 课程统一绘图风格。

一行启用（本地或 Colab 均可）：

    import ai4m_style as ai4m
    ai4m.use()

`use()` 会做三件事：
  1. 应用同目录下的 ``ai4m.mplstyle``（版式与配色，见该文件注释）；
  2. 注册三个课程色图 ``ai4m``（顺序）、``ai4m_div``（发散）、``ai4m_heat``（密度）；
  3. 返回配色对象 ``C``，方便在单条曲线上显式取色：``color=ai4m.C.crimson``。

配色与课程网站同源，截图、网页、幻灯片保持同一套视觉识别。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

__all__ = ["use", "C", "COLORS", "CYCLE", "cmap", "use_chinese_font", "style_path"]

STYLE_FILENAME = "ai4m.mplstyle"

# 与 website/assets/style.css 中的设计变量一一对应。
COLORS: Dict[str, str] = {
    "navy": "#16324f",        # 主色：模型 / 主曲线
    "navy_light": "#244b73",  # 主色浅调：次要曲线、拟合带
    "crimson": "#8c2d19",     # 强调：真实值、异常点、警示
    "gold": "#b45309",        # 次强调：采集函数、阈值
    "teal": "#0f766e",        # 对照组、第二类别
    "steel": "#4e7ca8",
    "taupe": "#9a6a4f",
    "sage": "#52796f",
    "slate": "#6b7280",       # 中性：辅助线、注释
    "paper": "#faf9f5",       # 画布底色（与网站纸张色一致）
    "ink": "#1e293b",         # 正文字色
    "muted": "#cbd5e1",       # 网格线
}

# 默认循环色序（与 ai4m.mplstyle 的 axes.prop_cycle 保持一致）
CYCLE: List[str] = [
    COLORS["navy"],
    COLORS["crimson"],
    COLORS["teal"],
    COLORS["gold"],
    COLORS["steel"],
    COLORS["taupe"],
    COLORS["sage"],
    COLORS["slate"],
]


class _Palette:
    """让 ``ai4m.C.navy`` 这样的写法可用，同时保留 ``C["navy"]``。"""

    def __init__(self, colors: Dict[str, str]) -> None:
        self.__dict__.update(colors)

    def __getitem__(self, key: str) -> str:
        return self.__dict__[key]

    def __iter__(self) -> Iterable[str]:
        return iter(self.__dict__.values())

    def __repr__(self) -> str:  # pragma: no cover - 交互式查看用
        return "AI4M palette: " + ", ".join(
            "%s=%s" % (k, v) for k, v in self.__dict__.items()
        )


C = _Palette(COLORS)

_CMAPS = {
    # 顺序：纸张底色 → 深海蓝。适合密度、概率、热力图。
    "ai4m": [COLORS["paper"], "#9db8d2", COLORS["navy_light"], COLORS["navy"]],
    # 发散：暗红 ← 中性 → 青绿。适合残差、SHAP 值、相关系数矩阵。
    "ai4m_div": [COLORS["crimson"], "#d9a08f", "#f2f0ea", "#7fc0b5", COLORS["teal"]],
    # 密度：纸张 → 金棕 → 暗红。适合 parity plot 的点密度、计数直方图。
    "ai4m_heat": [COLORS["paper"], "#e8c89a", COLORS["gold"], COLORS["crimson"]],
}


def style_path() -> Path:
    """``ai4m.mplstyle`` 的绝对路径（与本模块同目录）。"""
    return Path(__file__).resolve().parent / STYLE_FILENAME


def _register_cmaps() -> None:
    for name, stops in _CMAPS.items():
        for full_name, colors in ((name, stops), (name + "_r", list(reversed(stops)))):
            if full_name in plt.colormaps():
                continue
            created = LinearSegmentedColormap.from_list(full_name, colors)
            # Matplotlib 3.5 起推荐 mpl.colormaps.register；旧版回退到 cm.register_cmap。
            try:
                mpl.colormaps.register(created, name=full_name)
            except AttributeError:  # pragma: no cover - matplotlib < 3.5
                mpl.cm.register_cmap(name=full_name, cmap=created)


def cmap(name: str = "ai4m"):
    """按名字取课程色图，必要时先注册。"""
    _register_cmaps()
    return plt.get_cmap(name)


def use_chinese_font(verbose: bool = True) -> Optional[str]:
    """需要中文标注时调用：挑一个系统里真实存在的中文字体。

    课程 Notebook 的坐标轴标签统一用英文（投稿、报告都直接可用），
    只有在课堂演示里想写中文标题时才需要这一步。找不到中文字体时
    返回 None 并提示，而不是让 matplotlib 画出一堆豆腐块。
    """
    from matplotlib import font_manager

    candidates = [
        "Noto Sans CJK SC", "Noto Sans SC", "Source Han Sans SC",
        "Microsoft YaHei", "SimHei", "PingFang SC", "Heiti SC", "WenQuanYi Zen Hei",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name] + list(plt.rcParams["font.sans-serif"])
            plt.rcParams["axes.unicode_minus"] = False
            if verbose:
                print("中文字体已启用：%s" % name)
            return name
    if verbose:
        print(
            "未找到中文字体。Colab 上可运行："
            "!apt-get -qq install fonts-noto-cjk 然后重启运行时后重试。"
        )
    return None


def use(chinese: bool = False, verbose: bool = False) -> _Palette:
    """应用课程绘图风格，返回配色对象。

    参数
    ----
    chinese : 是否同时启用中文字体（默认关闭，坐标轴走英文）。
    verbose : 打印实际加载的样式文件路径，排查“样式没生效”时有用。
    """
    path = style_path()
    if path.exists():
        plt.style.use(str(path))
    else:  # 单独拷走 ai4m_style.py 时的兜底：直接写入关键 rcParams
        plt.rcParams.update({
            "figure.figsize": (5.2, 3.6),
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "font.size": 9.5,
            "axes.labelsize": 10.5,
            "axes.titlesize": 11.5,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.titlecolor": COLORS["navy"],
            "axes.edgecolor": "#475569",
            "axes.linewidth": 0.9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.axisbelow": True,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "grid.color": COLORS["muted"],
            "grid.linewidth": 0.6,
            "grid.alpha": 0.55,
            "legend.frameon": False,
            "lines.linewidth": 1.9,
            "lines.markersize": 5.5,
            "axes.prop_cycle": mpl.cycler(color=CYCLE),
        })
        if verbose:
            print("未找到 %s，已使用内置兜底 rcParams。" % STYLE_FILENAME)

    _register_cmaps()
    if chinese:
        use_chinese_font(verbose=True)
    if verbose and path.exists():
        print("已加载课程绘图风格：%s" % path)
    return C


def _ensure_importable() -> None:
    """在模块子目录（如 ``04 - Bayesian Optimization/``）里运行时补上搜索路径。"""
    root = str(Path(__file__).resolve().parent)
    if root not in sys.path:
        sys.path.insert(0, root)


_ensure_importable()
