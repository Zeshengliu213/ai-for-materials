# 02 — 监督学习（Supervised Learning）

在第一讲完成分子数据清洗、探索性可视化与 RDKit 描述符/分子指纹提取之后，本模块正式进入机器学习建模的核心：**如何从带实验标签的分子数据集中训练、验证、调优并解释监督学习模型**。

我们继续以贯穿前两讲的 **ESOL 水溶解度数据集**（1128 个分子的实测 $\log S$）为主线，并在最后将训练好的模型放到有机半导体稠环与改性分子（如并五苯 `pentacene`、`C8-BTBT`）上进行压力测试，直观暴露外推失效与表征盲区。

---

## 课程模块结构

| 序号 | Notebook | 核心内容 | 建议课时 |
|---|---|---|---|
| **02a** | `02a_regression.ipynb` | **回归入门**：问题形式化（$X \to y$）、训练/测试集划分与过拟合、评估指标（MAE / RMSE / $R^2$）与均值猜测基线、单特征到多特征线性回归、kNN 与特征标准化（`StandardScaler`）、树模型集成（随机森林 / 梯度提升）、描述符 vs 分子指纹（Bit / Count FP） | 60–75 min |
| **02b** | `02b_validation_and_tuning.ipynb` | **验证、调优与适用域**：单次划分的随机波动与 $K$ 折交叉验证（5-Fold CV）、数据泄漏（Data Leakage）与 `Pipeline` 防护、网格搜索（`GridSearchCV`）超参数调优、面向共轭大分子的外推压力测试与基于 Tanimoto 相似度的适用域（Applicability Domain）诊断 | 50–60 min |
| **02c** | `02c_classification.ipynb` | **分类与基础特征重要性**：难溶分子筛查二分类任务定义、分层抽样（`stratify`）、准确率陷阱与混淆矩阵（TP/FP/TN/FN）、Precision / Recall / F1 / ROC-AUC、结合实验成本调节决策阈值、树分裂重要性（MDI）vs 置换重要性（Permutation Importance）、对照 Yalkowsky 方程分析模型漏报原因 | 50–60 min |
| **02d** | `02d_exercises.ipynb` | **第二讲基础巩固习题**：涵盖训练/测试集划分与均值基线、多元线性回归、特征标准化与 kNN、防泄漏 Pipeline 与 5 折交叉验证、`GridSearchCV` 调参、分层二分类与随机森林特征重要性的 8 道基础练习 | 30–45 min |
| **参考答案** | `solutions/02_supervised_solutions.ipynb`<br>`solutions/02_exercises_solutions.ipynb` | 分别汇总 `02a`–`02c` 随堂练习（9 道）与 `02d` 基础巩固习题（8 道）的完整可运行代码与物理化学解析 | 课后自查 |

---

## 与第一讲（01 - Basics）的前后呼应

本讲直接兑现了第一讲埋下的四处核心伏笔：
1. **单变量到多变量建模**（呼应 `01c`）：从 `MolLogP vs logS` 的单变量散点趋势线出发，扩展为 10 个物理化学描述符 + 2048 维 Morgan 指纹的多元非线性回归；
2. **不同特征量纲的标准化**（呼应 `01b` / `01c`）：解释为什么分子量（几百）和氢键给体数（个位数）直接放进 kNN 或 SVR 会导致距离计算失真，并通过 `make_pipeline(StandardScaler(), ...)` 实现无泄漏标准化；
3. **Bit 指纹 vs Count 指纹的实战差异**（呼应 `01d`）：在 `02a` 和 `02b` 中实测发现，0/1 Bit 指纹因为无法区分重复子结构数量，不仅在回归误差上劣于 Count 指纹，还会把并五苯与并四苯的 Tanimoto 相似度误判为 `1.000`；
4. **共线性特征对模型解释的干扰**（呼应 `01c`）：在 `02c` 中展示高度共线的 `MolWt` 与 `HeavyAtomCount`（$r = 0.97$）如何平摊随机森林的树分裂重要性（MDI），以及如何用置换重要性（Permutation Importance）还原 `MolLogP` 的真实主导地位。

---

## 核心实验基准速查（ESOL，`random_state=42`）

### 1. 回归任务（`02a` & `02b`）
- **Dummy 均值猜测基线**：Test RMSE = `2.421`，$R^2 = -0.002$
- **单变量线性回归（仅 `MolLogP`）**：Test RMSE = `1.132`，$R^2 = 0.781$
- **多元线性回归（10 个描述符）**：Test RMSE = `0.968`，$R^2 = 0.840$
- **kNN（$k=10$，未标准化 vs 标准化）**：Test RMSE 从 `0.955` 降至 `0.733`（经 `GridSearchCV` 调优至 $k=5$, `weights="distance"` 后进一步降至 `0.658`）
- **随机森林（10 个描述符）**：Test RMSE = `0.688`，$R^2 = 0.899$
- **随机森林（仅 2048 维 Bit 指纹 vs Count 指纹）**：Test RMSE 分别为 `1.093` vs `0.946`
- **随机森林（10 个描述符 + 2048 维指纹）**：Test RMSE 降至 `0.669 ~ 0.674`，$R^2 = 0.905$

### 2. 分类任务（`02c`，难溶阈值 $\log S < -4$，正类占比 28.6%）
- **Dummy 多数类基线（全猜可溶）**：Accuracy = `0.715`，但 Recall = `0.000`，F1 = `0.000`，ROC-AUC = `0.500`
- **随机森林分类器**：Accuracy = `0.903`，Precision = `0.852`，Recall = `0.800`，F1 = `0.825`，ROC-AUC = `0.955`

---

## 运行环境说明

- 数据集路径已自动兼容相对路径 `../01 - Basics/data/esol.csv` 与当前目录下的 `data/esol.csv`，无需重复拷贝数据文件。
- 所有图表坐标轴与图例均采用英文标注，确保在 Windows、macOS、Linux 及 Google Colab 下均不会出现中文字体方块乱码。
