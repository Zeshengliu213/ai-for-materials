"""Static site configuration: paths, site metadata and course module metadata."""

import os
from pathlib import Path
from typing import Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
# website/ 是课程仓库的子目录，仓库根目录本身就是课程内容所在。
COURSE_DIR = ROOT_DIR.parent
ASSETS_SRC = ROOT_DIR / "assets"
DIST_DIR = ROOT_DIR / "dist"
SLIDES_DIR = COURSE_DIR / "slides"

SITE_TITLE = "AI for Materials Science"
SITE_SUBTITLE = "材料人工智能实战课程 · 研究生课程门户"
SITE_DESCRIPTION = (
    "面向零编程基础材料/化学/物理研究生的一学期 AI 实战课程："
    "Python 科学计算、机器学习、贝叶斯优化、神经网络、生成模型与图神经网络，"
    "全部配套可运行的 Jupyter Notebook 课件与数据集。"
)
# Public base URL used for sitemap.xml, canonical links and Open Graph tags.
# Leave as "" to skip those tags; override per build with
#     python website/build.py --base-url https://example.github.io/ai-for-materials
# or by setting the AI4M_BASE_URL environment variable.
SITE_BASE_URL = os.environ.get("AI4M_BASE_URL", "").strip()


def set_base_url(url: str) -> None:
    """Override SITE_BASE_URL at build time (used by build.py --base-url)."""
    global SITE_BASE_URL
    SITE_BASE_URL = url.strip().rstrip("/")

# ---------------------------------------------------------------------------
# Google Colab integration.
#
# Colab can open a notebook straight from GitHub, which removes the
# "download then re-upload" step for students. Set GITHUB_REPO to
# "<owner>/<repo>" once the course is pushed to GitHub and every notebook page
# gets a one-click "Open in Colab" button automatically.
# ---------------------------------------------------------------------------
GITHUB_REPO = "Zeshengliu213/ai-for-materials"
GITHUB_BRANCH = "main"
# Path of the course/ folder *inside* the repository. The course directory is
# itself the repository root, so this is empty; set it to "course" if the
# course folder is ever nested inside a larger monorepo.
GITHUB_COURSE_PREFIX = ""

# Shared (content-addressed) directory for de-duplicated dataset downloads.
SHARED_FILES_DIRNAME = "_shared"

STATUS_ORDER = {"done": 0, "partial": 1, "todo": 2}

MODULE_META: Dict[str, Dict[str, object]] = {
    "01": {
        "zh_title": "Python 与化学/材料数据基础",
        "en_title": "Basics: Python, Pandas, Plotting & RDKit",
        "semester": "part1",
        "status": "done",
        "status_label": "已完成",
        "summary": "Python 速成、Pandas 数据清洗、科研绘图与 RDKit 分子表示（AqSolDB 有机半导体主线）。",
        "outline": [],
    },
    "02": {
        "zh_title": "监督学习与模型评估防坑",
        "en_title": "Supervised Learning & Validation",
        "semester": "part1",
        "status": "done",
        "status_label": "已完成",
        "summary": "回归建模、交叉验证与 Scaffold Split 防数据泄漏、分类模型与特征重要性。",
        "outline": [],
    },
    "03": {
        "zh_title": "无监督学习：化学空间与发现",
        "en_title": "Unsupervised Learning & Discovery",
        "semester": "part1",
        "status": "done",
        "status_label": "已完成",
        "summary": "PCA/t-SNE 降维、K-means/DBSCAN/Butina 聚类与 Science 钯二聚体催化剂发现复现。",
        "outline": [],
    },
    "04": {
        "zh_title": "贝叶斯优化与主动实验设计",
        "en_title": "Bayesian Optimization",
        "semester": "part1",
        "status": "done",
        "status_label": "已完成",
        "summary": "高斯过程回归（GPR）、Tanimoto 分子核、EI/UCB 采集函数与 Science 钯催化偶联反应主动实验设计。",
        "outline": [],
    },
    "05": {
        "zh_title": "特征工程、SHAP 与 3D 分子",
        "en_title": "Feature Engineering & Molecular Informatics",
        "semester": "part1",
        "status": "todo",
        "status_label": "待编写",
        "summary": "特征选择与 SHAP 归因分析、3D 分子构象生成与 PubChem API 实战。",
        "outline": [
            "<code>05a</code> 特征选择（方差过滤、相关性剪枝、递归特征消除）与 SHAP 归因分析：从“模型说得准”走向“模型说得清”。",
            "<code>05b</code> 3D 分子构象生成（RDKit ETKDG + MMFF 优化）、构象系综与 3D 描述符。",
            "<code>05b</code> PubChem PUG-REST API 实战：按名称/SMILES 批量抓取实验性质，补全第 01 讲留下的 Yalkowsky 熔点伏笔。",
        ],
    },
    "06": {
        "zh_title": "无机与晶体材料信息学",
        "en_title": "Materials Informatics",
        "semester": "part1",
        "status": "todo",
        "status_label": "待编写",
        "summary": "Pymatgen 晶体结构分析、MP/COD 数据库、模拟 XRD、凸包相图与高通量筛选。",
        "outline": [
            "<code>06a</code> Pymatgen 晶体结构操作：晶胞、对称性与空间群、超胞与缺陷构建。",
            "<code>06a</code> Materials Project API 与 COD 数据库：批量检索形成能、带隙与弹性常数。",
            "<code>06b</code> 模拟 XRD 谱图、热力学凸包相图（convex hull）与稳定性判据。",
            "<code>06b</code> SOAP / 元素组成描述符与高通量虚拟筛选流程。",
        ],
    },
    "07": {
        "zh_title": "神经网络与材料显微视觉 CNN",
        "en_title": "Neural Networks & CNNs",
        "semester": "part2",
        "status": "done",
        "status_label": "已完成",
        "summary": "PyTorch MLP、梯度下降与 MC Dropout 不确定性；卷积神经网络与显微图像识别。",
        "outline": [],
    },
    "08": {
        "zh_title": "序列模型、Transformer 与反应预测",
        "en_title": "Sequence Models & Transformers",
        "semester": "part2",
        "status": "done",
        "status_label": "已完成",
        "summary": "SMILES 语言模型、SMILES 增强与 NLL 异常检测、手写迷你 Transformer 与化学反应产物预测。",
        "outline": [],
    },
    "09": {
        "zh_title": "生成模型：分子设计到电镜超分",
        "en_title": "Generative Models",
        "semester": "part2",
        "status": "partial",
        "status_label": "09a/09b 就绪",
        "summary": "SELFIES 分子 VAE、定向生成与代理模型欺骗、电镜超分辨率与扩散模型。",
        "outline": [
            "<code>09c</code>（编写中）电镜图像超分辨率与扩散模型入门。",
        ],
    },
    "10": {
        "zh_title": "图神经网络（GNN）与机器学习势函数",
        "en_title": "Graph Neural Networks & MLIPs",
        "semester": "part2",
        "status": "partial",
        "status_label": "10a/10b 就绪",
        "summary": "手写分子 GNN、Chemprop D-MPNN 全课程模型大比拼、晶体 CGCNN 与 MACE 势函数。",
        "outline": [
            "<code>10c</code>（编写中）晶体图网络 CGCNN 与 MACE 机器学习势函数。",
        ],
    },
}

# ---------------------------------------------------------------------------
# Home-page knowledge roadmap: the conceptual path through the ten modules.
# Each stage lists the module numbers it covers; the modules themselves (and
# their completion status) are resolved at build time from MODULE_META, so a
# stage never drifts out of sync with the syllabus.
# ---------------------------------------------------------------------------

ROADMAP_STAGES: List[Dict[str, object]] = [
    {
        "icon": "stage-1",
        "title": "表示与数据",
        "desc": "把分子、实验记录与文献数据变成能计算的数字",
        "modules": ["01"],
    },
    {
        "icon": "stage-2",
        "title": "经典机器学习与防坑",
        "desc": "回归分类、交叉验证、Scaffold Split 与化学空间探索",
        "modules": ["02", "03"],
    },
    {
        "icon": "stage-3",
        "title": "贝叶斯主动实验",
        "desc": "高斯过程 + 采集函数：用更少的实验找到更好的材料",
        "modules": ["04"],
    },
    {
        "icon": "stage-4",
        "title": "描述符与材料信息学",
        "desc": "SHAP 归因、3D 构象、晶体结构与高通量筛选",
        "modules": ["05", "06"],
    },
    {
        "icon": "stage-5",
        "title": "深度学习表征",
        "desc": "神经网络、显微图像 CNN 与 SMILES 序列模型",
        "modules": ["07", "08"],
    },
    {
        "icon": "stage-6",
        "title": "生成模型与图网络",
        "desc": "分子生成、图神经网络与机器学习势函数",
        "modules": ["09", "10"],
    },
]

DEFAULT_META: Dict[str, object] = {
    "zh_title": "",
    "en_title": "",
    "semester": "part1",
    "status": "todo",
    "status_label": "待编写",
    "summary": "",
    "outline": [],
}


def module_meta(num: str, fallback_title: str) -> Dict[str, object]:
    """Return metadata for a module number, falling back to directory naming."""
    if num in MODULE_META:
        return MODULE_META[num]
    meta = dict(DEFAULT_META)
    meta["zh_title"] = fallback_title
    meta["en_title"] = fallback_title
    meta["semester"] = "part1" if int(num) <= 6 else "part2"
    return meta


def colab_url(module_dir_name: str, rel_path: str) -> str:
    """Build a Colab "open from GitHub" URL, or "" when GitHub is not configured."""
    if not GITHUB_REPO:
        return ""
    from urllib.parse import quote
    path = "/".join(
        quote(part) for part in [GITHUB_COURSE_PREFIX, module_dir_name, rel_path] if part
    )
    return (
        "https://colab.research.google.com/github/"
        f"{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{path}"
    )


def page_url(href: str) -> str:
    """Absolute URL of a dist-relative page, or "" when no base URL is set."""
    if not SITE_BASE_URL:
        return ""
    return "%s/%s" % (SITE_BASE_URL.rstrip("/"), href.lstrip("/"))
