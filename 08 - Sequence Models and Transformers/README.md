# 08 · 序列模型与化学语言模型（Sequence Models and Transformers）

本模块从一维化学字符串（SMILES）的表示特性出发，系统讲解自回归分子语言模型（RNN / LSTM）、SMILES 枚举数据增强、基于负对数似然的分布外探针、小样本领域迁移微调，以及编码器-解码器 Transformer 在化学反应产物预测中的应用。

## 课程文件结构

| 文件 | 内容定位 | 核心知识点 |
| :--- | :--- | :--- |
| `08a_smiles_language_model.ipynb` | 有机光电分子的自回归序列生成 | 化学感知正则分词、马尔可夫 Bigram 基线与远程语法约束、`SmilesRNN`（Embedding + LSTM + Linear）、教师强制训练与梯度裁剪、采样温度调控与构造单元保持 |
| `08b_smiles_lstm_aqsoldb.ipynb` | 真实数据库的枚举增强、似然探针与迁移微调 | 异构数据库 `AqSolDB` 清洗与 `Vocab` 封装、SMILES 枚举增强的原理与指标权衡、`NLL per token` 分布外探针、面向有机半导体的小样本迁移微调与灾难性遗忘 |
| `08c_reaction_transformer.ipynb` | 注意力机制与手写迷你 Transformer 反应预测 | 专家反应模板（SMARTS）vs. 无模板 Seq2Seq 翻译、缩放点积注意力与因果/填充掩码、正弦位置编码、`ReactionTransformer` 架构、交叉注意力热力图与 USPTO 真实专利反应解析 |
| `08d_exercises.ipynb` | 第 08 讲基础习题集（8 道自包含练习） | 正则分词还原、教师强制切片、Bigram 矩阵、LSTM 张量维度追踪、温度与信息熵、掩码交叉熵 NLL、因果自注意力、Suzuki 模板与 Canonical 精确匹配 |
| `solutions/08_sequence_solutions.ipynb` | 课堂练习参考解答（`08a` + `08b` + `08c`） | 主讲 Notebook 中全部课堂练习（`08a-1`~`08a-3`、`08b-1`~`08b-4`、`08c-1`~`08c-3`）的完整实现与化学讨论 |
| `solutions/08_exercises_solutions.ipynb` | 基础习题集参考解答（`08d`） | `08d_exercises.ipynb` 中 8 道基础编程练习的参考解答 |

## 建议学习顺序

1. 先按顺序阅读并运行 `08a` $\to$ `08b` $\to$ `08c`，动手尝试每节内嵌的课堂练习，再对照 `solutions/08_sequence_solutions.ipynb` 检验思路；
2. 完成 `08d_exercises.ipynb` 中的 8 道基础练习，巩固分词、张量切片、掩码损失与注意力机制的代码细节。
