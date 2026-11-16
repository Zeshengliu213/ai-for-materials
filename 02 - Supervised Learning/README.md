# 02 — 监督学习：经典机器学习算法原理与防坑实战（Supervised Learning）

在第一讲完成分子数据清洗、探索性可视化与 RDKit 描述符/分子指纹提取之后，本模块先通过全景导论（`020`）厘清**“到底什么是机器学习、它在材料科学中能解决哪五类问题、以及材料数据区别于互联网 AI 的专属陷阱”**；随后按“底层数学/几何直觉（拒绝黑箱）+ AqSolDB 与有机半导体真实实例”双线并重，把全部经典监督学习算法拆分为循序渐进的 `02a`–`02f` 六节实战。

全模块统一采用 **AqSolDB 水溶解度数据集**（`data/solubility.csv`，清洗后 **9,480 个有效分子、17 个 RDKit 物理化学描述符**），并在有机半导体稠环与侧链改性分子（如并苯系列、`BTBT`、`C8-BTBT`、`TIPS-Pentacene`）上进行外推压力测试与适用域诊断。

---

## 课程模块结构

| 序号 | Notebook | 核心算法原理（不靠黑箱） | 材料实例与伏笔兑现 | 建议课时 |
|---|---|---|---|---|
| **020** | `020_ml_for_materials_overview.ipynb` | AI $\supset$ ML $\supset$ DL、从“写公式”到“学规律”反转、内插 vs 外推矛盾 | D–$\pi$–A 有机光电空间估算、五大材料 AI 场景映射、课题选型自测 | 30–40 min |
| **02a** | `02a_linear_models.ipynb` | 最小二乘几何直观、**8 行 NumPy 手写梯度下降**、多项式偏差–方差权衡、**Ridge ($L_2$) vs Lasso ($L_1$)** 正则化路径 | `MolLogP` 单变量 $\to$ 17 描述符 OLS 共线性权重正负反转破案与正则化驯服 | 50–60 min |
| **02b** | `02b_knn_and_svm.ipynb` | 二维平面 **kNN 找邻居连线**、特征缩放几何机制、**SVM 最大间隔超平面、软间隔 $C$、$\epsilon$-管道与 RBF 核技巧** | `(MolLogP, MolWt)` 平面上萘的真假邻居对比、RBF-SVR 溶解度非线性等高线 | 50–60 min |
| **02c** | `02c_trees_and_ensembles.ipynb` | **12 行 NumPy 手算决策树最优切分（MSE）**、阶梯函数切分图、**Bagging（随机森林降方差）vs Boosting（XGBoost 拟合残差降偏差）** | 描述符 vs Bit/Count Morgan 指纹大比拼；并苯系列（苯 $\to$ 并五苯）揭示树模型外推截断本质 | 60–70 min |
| **02d** | `02d_classification.ipynb` | **10 行 NumPy 手写感知机**（判错挪直线）$\to$ **Sigmoid 与逻辑回归概率**、混淆矩阵、Precision/Recall/F1/ROC-AUC 与阈值移动 | 难溶分子（$\log S < -4$）筛查、`C8-BTBT` 溶剂先验边界、MDI vs 置换重要性、Yalkowsky 方程与离子盐/刚性晶体错分破案 | 55–65 min |
| **02e** | `02e_validation_and_tuning.ipynb` | 5 折交叉验证、**`Pipeline` 防预处理泄漏对照实测**、`GridSearchCV` 与学习曲线（`learning_curve`） | 随机划分 vs **Murcko 骨架划分（Scaffold Split）** vs 跨环数尺寸外推；Tanimoto **适用域**体检 | 50–60 min |
| **02f** | `02f_exercises.ipynb` | 覆盖 `02a`–`02e` 全部经典回归/分类模型、阈值调节、防泄漏流水线与骨架划分的 8 道综合实战习题 | 统一基于 AqSolDB 实测核对 | 35–45 min |
| **参考答案** | `solutions/02_supervised_solutions.ipynb`<br>`solutions/02_exercises_solutions.ipynb` | 分别汇总 `02a`–`02e` 全部 **10 道随堂练习**与 `02f` 全部 **8 道综合习题**的完整可运行代码、图表与物理化学解析 | 课后自查 | — |

---

## 核心实验基准速查（AqSolDB 9,480 分子，`random_state=42`）

### 1. 回归任务（`02a`、`02b`、`02c`、`02e`）
- **Dummy 均值猜测基线**：Test RMSE = `2.420`，$R^2 = 0.000$
- **单特征线性回归（仅 `MolLogP`）**：Test RMSE = `1.885`，$R^2 = 0.393$
- **17 描述符多元线性回归（OLS / Ridge）**：Test RMSE = `1.636 ~ 1.649`，$R^2 \approx 0.54$
- **kNN（$k=5$，未标准化 vs 标准化）**：Test RMSE 从 `1.561` 骤降至 **`1.241`**（经 `Pipeline + GridSearchCV` 距离加权调优后进一步降至 **`1.186`**）
- **RBF 核支持向量回归（`SVR`，标准化）**：Test RMSE = **`1.231`**，$R^2 = 0.741$
- **单棵不限深度决策树 vs 随机森林 vs XGBoost（17 描述符）**：Test RMSE 从单棵深树的 `1.531`（严重过拟合）降至随机森林 **`1.168`** 与 XGBoost **`1.153`**（$R^2 = 0.773$）
- **XGBoost 分子表示对比**：2048 Bit 指纹（`1.431`）$\to$ 2048 Count 指纹（`1.273`）$\to$ 17 描述符（`1.173`）$\to$ **17 描述符 + 2048 Count 指纹组合（`1.106`，$R^2 = 0.791$）**

### 2. 二分类筛查任务（`02d`，难溶阈值 $\log S < -4.0$，正类占比 28.6%）
- **Dummy 多数类基线（全猜可溶）**：Accuracy = `0.715`，但 Recall = `0.000`，F1 = `0.000`，ROC-AUC = `0.500`
- **感知机（Perceptron）$\to$ 逻辑回归（Logistic Regression）**：F1 从 `0.672` 升至 `0.710`（ROC-AUC = `0.892`）
- **随机森林 / XGBoost 分类器**：Accuracy = `0.890 ~ 0.896`，F1 = `0.797 ~ 0.808`，ROC-AUC = **`0.952 ~ 0.956`**

---

## 运行环境说明

- 数据集自动读取 `data/solubility.csv`（兼容 `../01 - Basics/data/solubility.csv`），本地 `zesheng` 环境与 Google Colab 均可直接运行。
- 所有图表均启用课程统一出版级绘图样式 `ai4m.mplstyle`，坐标轴与图例统一采用英文标注，杜绝跨平台中文字体乱码。
