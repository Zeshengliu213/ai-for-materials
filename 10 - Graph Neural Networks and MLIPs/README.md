# 第十部分：图神经网络与机器学习势函数

结构仿照 EPFL CH-457 *AI for Chemistry*（[schwallergroup/ai4chem_course](https://github.com/schwallergroup/ai4chem_course)）的 `03 - Intro to Deep Learning`，三个 notebook 一一对应。数据继续用第一、二部分的 AqSolDB，测试集和第二部分**完全相同**，所以所有模型的结果可以直接放在一起比较。

| Notebook | 内容 | 对应 ai4chem |
|---|---|---|
| `03a_neural_networks.ipynb` | 神经元和激活函数；张量和自动求导；手写梯度下降拟合 logS–logP；Python 的类和 `nn.Module`；训练 / 验证 / 测试三个集合；`DataLoader` 小批量；训练循环；过拟合、早停、Dropout、权重衰减；学习率 | `01_intro_to_dl.ipynb` |
| `03b_graph_neural_networks.ipynb` | 归纳偏置；分子图（原子特征、键特征、`edge_index`）；在联噻吩上手算消息传递和感受野；读出和置换不变性；用纯 PyTorch 写 GNN（约 50 行）；批处理；训练并比较；并苯系列外推 | `02_graph_nns.ipynb` |
| `03c_chemprop.ipynb` | D-MPNN 和 10a 的区别；`chemprop train` / `chemprop predict`；用 `--splits-file` 保证同一个测试集；第二、三部分所有模型的总比较；预测有机半导体分子 | `03_gnn_simple_example.ipynb` |
| `solutions/10_gnn_solutions.ipynb` | 全部 8 道 🏋️ 练习的参考答案 | — |
| `data/solubility.csv` | 和第一、二部分同一份 AqSolDB 数据 | 替代 ESOL |

建议顺序是 07a → 10a → 10b。07a、10a 各约 2 小时，10b 约 1 小时。

## 和 ai4chem 的区别

- **不用 PyTorch Lightning、wandb、PyG、OGB、DeepChem**。07a、10a 只用纯 PyTorch，训练循环和消息传递都一行一行写出来；10b 只需要 `pip install chemprop`。Colab 上不用注册任何账号。
- **GNN 自己写**。原课程直接调用 PyG 的 `NNConv`；这里用 `index_add_` 实现消息聚合和读出，学生能看到 GNN 里没有任何魔法。结尾再介绍 PyG、DGL、chemprop。
- **补了原课程没讲的东西**：手写梯度下降、验证集的作用、Dropout 和权重衰减、学习率的影响、批处理怎么把多个分子拼成一张图、置换不变性的实测、感受野、D-MPNN 为什么用有向边。
- **chemprop 和自己的模型用同一个测试集**。原课程让 chemprop 自己随机划分，结果没法和前面比较。
- 讲解用中文，图上的文字用英文。标记和前两部分一致：📘 🤔 ▶️ ✏️ 🏋️ 💡。

## 和前两部分的呼应

| 前面埋下的伏笔 | 第三部分在哪里兑现 |
|---|---|
| 01d：Morgan 指纹看的是每个原子周围几根键的环境 | 10a 第 3 节：GNN 就是"可学习的 Morgan 指纹"，层数 = 半径 |
| 01d：同一个分子有多种 SMILES | 10a 第 1 节：随机 SMILES；第 5.4 节：打乱原子编号，GNN 输出不变 |
| 02a：随机森林把并五苯预测得和并四苯一样 | 10a 第 7 节：求和读出的 GNN 延续了趋势；练习 10a-3：换成平均读出 |
| 02b：调参的效果小于随机种子的波动；scaffold split | 07a 第 6 节：网络大 50 倍，测试 RMSE 几乎不变；练习 10b-2：chemprop 的 scaffold split |
| 02c：Yalkowsky 方程，熔点信息不在描述符里 | 07a 第 3 节：梯度下降拟合 logS–logP 的斜率；07a 第 6 节："瓶颈在特征，不在模型" |
| 02c：C8-BTBT 在水里仍然难溶 | 10b 第 5 节：chemprop 预测侧链让水溶解度变差 |

## 主要结果（同一个测试集，1896 个分子）

| 模型 | 输入 | 测试 RMSE |
|---|---|---|
| 永远预测平均值 | — | 2.42 |
| 随机森林（02a） | 17 个描述符 | 1.17 |
| MLP 64×64（07a） | 17 个描述符 | 1.19 |
| MLP 512×512，最后一轮 / 早停 / Dropout + 权重衰减 + 早停（07a） | 17 个描述符 | 1.18 / 1.17 / 1.17 |
| 随机森林（02a） | 描述符 + 计数指纹 | 1.11 |
| 自己写的 GNN，3 层，60 轮（10a） | 只有原子和键 | 1.04 |
| chemprop D-MPNN，30 轮（10b） | 只有原子和键 | 1.05（R² 0.81） |

其他值得在课上讨论的数字：

- 07a：梯度下降拟合 logS = w·logP + b，得到 w ≈ -0.41，和 `np.polyfit` 一致，但比 Yalkowsky 的 -1 平缓得多。
- 07a：512×512 的 MLP 训练 RMSE 0.58、最后一轮验证 RMSE 1.44，但测试 RMSE 只有 1.18。小验证集（759 个）对少数离谱的预测非常敏感。
- 10a：并苯系列 GNN 预测 -1.38、-3.73、-5.85、-7.22、-7.78（并五苯不在数据集里）；随机森林在并四苯、并五苯处几乎走平（-8.27、-8.38）。
- 练习 10a-2 / 10a-3：GNN 1 层 1.12、5 层 1.03（各 40 轮）；平均读出 1.26，比求和读出差很多，但并苯趋势仍在。
- 练习 07a-3 / 10b-1：分类 ROC-AUC，MLP 0.941、chemprop 0.944，都没有超过 02c 的随机森林（0.953）。练习 10b-2：chemprop 的 scaffold split 测试 RMSE 1.05，和随机划分一样。
- 不加 `torch.use_deterministic_algorithms(True)` 时，同样代码和种子跑两次，平均读出 GNN 的测试 RMSE 分别是 1.15 和 1.24（`index_add_` 的多线程加法顺序不固定）。所以 07a、10a 的 `set_seed` 里都加了这一行。
- 10b：chemprop 预测噻吩 -1.43（实验 -1.45）、3-己基噻吩 -4.93、BTBT -6.35、C8-BTBT -7.49。

## 运行环境

- 本地：Python ≥ 3.10，需要 `numpy pandas matplotlib scikit-learn rdkit torch`；10b 还需要 `chemprop`（2.x 版本）
- Colab：PyTorch 已预装；每个 notebook 第一格会在需要时自动安装 RDKit 或 chemprop
- 全部在 CPU 上运行，不需要 GPU
- 数据：本地读 `data/solubility.csv`；在 Colab 上如果找不到文件，会弹出上传按钮
- 运行时间（16 核 CPU）：07a 约 2 分钟，10a 约 2.5 分钟，10b 约 4 分钟，参考答案约 10 分钟
- 10b 会在 notebook 所在的文件夹里生成 `chemprop_data/` 和 `chemprop_runs/` 两个文件夹（数据副本、日志、模型），可以随时删除

## 验证情况

4 个 notebook 都在 Python 3.12、PyTorch 2.8（CPU）、scikit-learn 1.8、pandas 3.0、RDKit 2025.09.6、chemprop 2.2.3 下从头到尾运行通过，没有报错。正文里引用的数字都已经和这次运行的结果核对过。所有训练都固定了随机种子并开启了确定性算法（chemprop 用 `--pytorch-seed 0`），同一台电脑上重复运行结果完全一样（已实测）；换了 PyTorch 版本或 CPU，结果可能在小数点后第二位有差别，正文里用"约"表示。

第二部分用过的 conda 环境 `zesheng` 这次**没有**验证：里面的 PyTorch 2.2.2 是用 NumPy 1.x 编译的，和环境里的 NumPy 2.2.6 不兼容，`import torch` 就会报错。要在这个环境里运行第三部分，需要先把 NumPy 降到 2.0 以下，或者把 PyTorch 升级到 2.3 以上。
