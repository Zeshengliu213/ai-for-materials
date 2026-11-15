# AI for Materials Science（零基础材料研究生 · 一学期实战课程）

本课程面向**零编程基础的材料、化学、物理相关专业研究生**，融合了林雪平大学（LiU）*AI for Materials Science* 的宏观教学脉络与 EPFL CH-457 的互动实战设计，全程使用 **Python + Scikit-Learn + RDKit + Pymatgen + PyTorch**，纯 CPU 即可在本地或 Google Colab 流畅运行。

---

## 课程总目录（共 10 大模块 · 上/下半学期平滑进阶）

### 上半学期：科学计算、经典机器学习与材料信息学

| 模块 | 主题 | 核心内容与实战 Notebook | 状态 |
| :--- | :--- | :--- | :--- |
| **01** | **Python 与化学/材料数据基础** | `01a` Python 速成 · `01b` Pandas · `01c` 可视化 · `01d` RDKit 分子表示（AqSolDB 有机半导体主线） | ✅ 已完成 |
| **02** | **监督学习与模型评估防坑** | `02a` 回归 · `02b` 交叉验证/Scaffold Split/适用域 · `02c` 分类与特征重要性 | ✅ 已完成 |
| **03** | **无监督学习：化学空间与发现** | `03a` PCA/t-SNE 降维 · `03b` K-means/DBSCAN/Butina 聚类 · `03c` *Science* 钯二聚体催化剂发现 | ✅ 已完成 |
| **04** | **贝叶斯优化与主动实验设计** | `04a` 从零理解高斯过程回归（GPR）与不确定性 · `04b` EI/UCB 采集函数与实验条件寻优 | 🚧 待编写 |
| **05** | **特征工程、SHAP 与 3D 分子** | `05a` 特征选择与 SHAP 归因分析 · `05b` 3D 分子构象与 PubChem API（补全 Yalkowsky 熔点伏笔） | 🚧 待编写 |
| **06** | **无机与晶体材料信息学** | `06a` Pymatgen 晶体/MP 与 COD 数据库 · `06b` 模拟 XRD、热力学凸包相图、SOAP 与高通量筛选 | 🚧 待编写 |

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

## ☁️ 在线运行（Google Colab）

零基础同学无需在本地安装 Python，点击下方任意章节的 **Open in Colab** 徽章即可直接在浏览器运行：

| 章节 | Notebook | 在线运行 |
| :--- | :--- | :--- |
| `01 - Basics` | `01a_python_crash_course.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/01%20-%20Basics/01a_python_crash_course.ipynb) |
| `01 - Basics` | `01b_pandas.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/01%20-%20Basics/01b_pandas.ipynb) |
| `01 - Basics` | `01c_plotting.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/01%20-%20Basics/01c_plotting.ipynb) |
| `01 - Basics` | `01d_rdkit_basics.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/01%20-%20Basics/01d_rdkit_basics.ipynb) |
| `02 - Supervised Learning` | `02a_regression.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/02a_regression.ipynb) |
| `02 - Supervised Learning` | `02b_validation_and_tuning.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/02b_validation_and_tuning.ipynb) |
| `02 - Supervised Learning` | `02c_classification.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zeshengliu213/ai-for-materials/blob/main/02%20-%20Supervised%20Learning/02c_classification.ipynb) |
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
