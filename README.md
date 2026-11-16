# AI for Materials Science（零基础材料研究生 · 一学期实战课程）

本课程面向**零编程基础的材料、化学、物理相关专业研究生**，融合了林雪平大学（LiU）*AI for Materials Science* 的宏观教学脉络与 EPFL CH-457 的互动实战设计，全程使用 **Python + Scikit-Learn + RDKit + Pymatgen + PyTorch**，纯 CPU 即可在本地或 Google Colab 流畅运行。

---

## 课程总目录（共 10 大模块 · 上/下半学期平滑进阶）

### 上半学期：科学计算、经典机器学习与材料信息学

| 模块 | 主题 | 核心内容与实战 Notebook | 状态 |
| :--- | :--- | :--- | :--- |
| **01** | **Python 与化学/材料数据基础** | `01a` Python 速成 · `01b` Pandas · `01c` 可视化 · `01d` RDKit 分子表示（AqSolDB 有机半导体主线） | ✅ 已完成 |
| **02** | **监督学习与模型评估防坑** | `020` 材料 ML 总论 · `02a` 线性/梯度下降/Ridge&Lasso · `02b` kNN/SVM · `02c` 决策树/RF/XGBoost · `02d` 感知机/逻辑回归/分类归因 · `02e` 交叉验证/Scaffold Split/适用域 | ✅ 已完成 |
| **03** | **无监督学习：化学空间与发现** | `03a` 手算 PCA/载荷与 t-SNE 降维 · `03b` 手写 K-means/DBSCAN/层次聚类/Butina · `03c` *Science* 钯二聚体催化剂发现 | ✅ 已完成 |
| **04** | **贝叶斯优化与主动实验设计** | `04a` 从零理解高斯过程回归（GPR）与不确定性 · `04b` EI/UCB 采集函数与实验条件寻优 | 🚧 待编写 |
| **05** | **特征工程、SHAP 与 3D 分子** | `05a` 特征选择与 SHAP 归因分析 · `05b` 3D 分子构象与 PubChem API（补全 Yalkowsky 熔点伏笔） · `05c` 基础习题 | ✅ 已完成 |
| **06** | **无机与晶体材料信息学** | `06a` Pymatgen 晶体结构、对称性与 COD/MP 数据库 · `06b` 模拟 XRD、热力学凸包、容差因子、组成描述符与高通量筛选 · `06c` 基础习题 | ✅ 已完成 |

### 下半学期：材料深度学习、生成模型与图神经网络（全 PyTorch）

| 模块 | 主题 | 核心内容与实战 Notebook | 状态 |
| :--- | :--- | :--- | :--- |
| **07** | **神经网络与材料显微视觉 CNN** | `07a` PyTorch MLP、梯度下降与 MC Dropout · `07b` 卷积神经网络（CNN）与显微组织图像识别 | 🟡 `07a` 就绪，`07b` 待写 |
| **08** | **序列模型、Transformer 与反应预测** | `08a` SMILES 语言模型（CEP）· `08b` SMILES 增强与 NLL 异常检测 · `08c` 手写迷你 Transformer 与 Suzuki 偶联反应预测 | 🟡 `08a`/`08b` 就绪，`08c` 待写 |
| **09** | **生成模型：分子设计到电镜超分** | `09a` SELFIES 分子 VAE · `09b` 定向生成与代理模型欺骗 · `09c` 电镜去噪自编码器、超分辨率与扩散模型 | 🟡 `09a`/`09b` 就绪，`09c` 待写 |
| **10** | **图神经网络（GNN）与机器学习势函数** | `10a` 50 行纯 PyTorch 手写分子 GNN · `10b` Chemprop D-MPNN（全课程模型大比拼）· `10c` 晶体 CGCNN 与 MACE 势函数 | 🟡 `10a`/`10b` 就绪，`10c` 待写 |

---

## Notebook 互动标记说明

| 标记 | 含义 | 学习动作 |
|---|---|---|
| 📘 | 讲解 | 仔细阅读物理/化学背景与原理 |
| 🤔 | 先猜一猜 | **运行代码之前**先思考会输出什么 |
| ▶️ | 运行看看 | 选中代码格，按 `Shift + Enter` |
| ✏️ | 改一改 | 修改标有 `# ✏️` 的参数后重新运行 |
| 🏋️ | 练习 | 独立编写代码（参考答案在各章 `solutions/` 文件夹） |
| 💡 | 小贴士 | 实用的工程技巧或伏笔提示 |

## 🎨 统一科研绘图风格（ai4m.mplstyle）

课程自带一套与[课程网站](../website/)同源的 Matplotlib 风格，让每份 Notebook 跑出来的图
直接是可投稿的版式：配色为深海蓝 `#16324f` / 学院暗红 `#8c2d19` / 青绿 `#0f766e` /
金棕 `#b45309`，去掉上、右边框，只保留横向浅灰网格，标题左对齐加粗，图例无边框，
`savefig` 默认 300 dpi。

在任意 Notebook 的 import 之后加两行即可（本地与 Colab 通用）：

```python
import pathlib, sys
sys.path.insert(0, str(pathlib.Path.cwd().parent))   # course/ 根目录
import ai4m_style as ai4m

C = ai4m.use()        # 应用风格，返回课程配色
```

之后：

- 多条曲线自动按课程色序上色，不用手动指定；
- 需要点名某个颜色时写 `color=C.crimson`（可用 `navy / navy_light / crimson / gold /
  teal / steel / taupe / sage / slate / ink / muted`）；
- 三个课程色图可直接用名字取：`cmap="ai4m"`（顺序，适合密度/概率）、
  `cmap="ai4m_div"`（发散，适合残差与 SHAP）、`cmap="ai4m_heat"`（密度/计数），
  每个都有对应的 `_r` 反序版本；
- 坐标轴标签统一用英文（投稿、组会直接可用）；课堂演示要写中文时调用
  `ai4m.use(chinese=True)`，它会在系统里挑一个真实存在的中文字体，
  找不到就明确提示而不是画出一堆豆腐块。

只想要版式、不想 import 模块时，也可以直接 `plt.style.use("../ai4m.mplstyle")`。

### 批量注入到所有 Notebook

```bash
python apply_style.py            # 预演：列出会改哪些文件
python apply_style.py --write    # 真正写入（幂等，可重复运行）
```

脚本会把上面那两行放到每份 Notebook 的 import 之后。注意：**已保存的旧图仍是旧风格**，
需要 Restart & Run All 重跑一遍才会刷新。

## ☁️ 在线运行（Google Colab）

零基础同学无需在本地安装 Python，点击下方任意章节的 **Open in Colab** 徽章即可直接在浏览器运行：

| 章节 | Notebook | 在线运行 |
| :--- | :--- | :--- |
| `01 - Basics` | `01a_python_crash_course.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/01%20-%20Basics/01a_python_crash_course.ipynb) |
| `01 - Basics` | `01b_pandas.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/01%20-%20Basics/01b_pandas.ipynb) |
| `01 - Basics` | `01c_plotting.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/01%20-%20Basics/01c_plotting.ipynb) |
| `01 - Basics` | `01d_rdkit_basics.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/01%20-%20Basics/01d_rdkit_basics.ipynb) |
| `02 - Supervised Learning` | `020_ml_for_materials_overview.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/020_ml_for_materials_overview.ipynb) |
| `02 - Supervised Learning` | `02a_linear_models.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/02a_linear_models.ipynb) |
| `02 - Supervised Learning` | `02b_knn_and_svm.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/02b_knn_and_svm.ipynb) |
| `02 - Supervised Learning` | `02c_trees_and_ensembles.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/02c_trees_and_ensembles.ipynb) |
| `02 - Supervised Learning` | `02d_classification.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/02d_classification.ipynb) |
| `02 - Supervised Learning` | `02e_validation_and_tuning.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/02e_validation_and_tuning.ipynb) |
| `02 - Supervised Learning` | `02f_exercises.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/02f_exercises.ipynb) |
| `03 - Unsupervised Learning` | `03a_dimensionality_reduction.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/03%20-%20Unsupervised%20Learning/03a_dimensionality_reduction.ipynb) |
| `03 - Unsupervised Learning` | `03b_clustering.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/03%20-%20Unsupervised%20Learning/03b_clustering.ipynb) |
| `03 - Unsupervised Learning` | `03c_pd_dimer_discovery.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/03%20-%20Unsupervised%20Learning/03c_pd_dimer_discovery.ipynb) |
| `04 - Bayesian Optimization` | `04a_gaussian_processes.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/04%20-%20Bayesian%20Optimization/04a_gaussian_processes.ipynb) |
| `04 - Bayesian Optimization` | `04b_bayesian_optimization.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/04%20-%20Bayesian%20Optimization/04b_bayesian_optimization.ipynb) |
| `07 - Neural Networks and CNNs` | `07a_neural_networks.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/07%20-%20Neural%20Networks%20and%20CNNs/07a_neural_networks.ipynb) |
| `08 - Sequence Models and Transformers` | `08a_smiles_language_model.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/08%20-%20Sequence%20Models%20and%20Transformers/08a_smiles_language_model.ipynb) |
| `08 - Sequence Models and Transformers` | `08b_smiles_lstm_aqsoldb.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/08%20-%20Sequence%20Models%20and%20Transformers/08b_smiles_lstm_aqsoldb.ipynb) |
| `09 - Generative Models` | `09a_vae_selfies.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/09%20-%20Generative%20Models/09a_vae_selfies.ipynb) |
| `09 - Generative Models` | `09b_goal_directed_generation.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/09%20-%20Generative%20Models/09b_goal_directed_generation.ipynb) |
| `10 - Graph Neural Networks and MLIPs` | `10a_graph_neural_networks.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/10%20-%20Graph%20Neural%20Networks%20and%20MLIPs/10a_graph_neural_networks.ipynb) |
| `10 - Graph Neural Networks and MLIPs` | `10b_chemprop.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/10%20-%20Graph%20Neural%20Networks%20and%20MLIPs/10b_chemprop.ipynb) |

> **教师发布提示**：上传到 GitHub 前，在 `course/` 目录执行 `python configure_colab.py <你的GitHub用户名> <仓库名>` 即可一键更新所有链接。
