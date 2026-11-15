# 第七讲：神经网络与材料显微视觉 CNN（Neural Networks & CNNs）

本讲是课程下半学期（深度学习与前沿生成/图模型）的开篇模块。我们先使用纯 PyTorch 从单个神经元和手写梯度下降出发，搭建多层感知机（MLP）并在与第 02 讲完全一致的 AqSolDB 测试集上对比深度网络与随机森林的边界；随后进入深度学习真正发挥表征优势的领域——使用二维卷积神经网络（CNN）分析材料显微组织（SEM/金相）图像。

## 课件与习题结构

| Notebook | 核心内容 |
|---|---|
| `07a_neural_networks.ipynb` | 人工神经元与非线性激活函数（ReLU/Sigmoid/Tanh）；PyTorch 张量与 Autograd 自动求导；手写梯度下降拟合 Yalkowsky $\log S - \log P$ 关系；Python `class` 与 `nn.Module` 封装；训练/验证/测试划分与 `DataLoader`；过拟合诊断与早停、Dropout、权重衰减；MC Dropout 不确定性估计；学习率动力学与二分类扩展 |
| `07b_cnn_microstructure.ipynb` | 为什么展平 MLP 在二维显微图像上会遭遇参数爆炸与平移失配；二维离散卷积与平滑/Sobel 相界边缘提取算子；`nn.Conv2d`、`MaxPool2d` 与全局平均池化 `AdaptiveAvgPool2d`；四类典型合成金相微结构（球状析出相、层片珠光体、凝固枝晶、多晶晶界）CNN vs. MLP 分类对比；物理合规的旋转/翻转数据增强；特征图可视化与析出相面积分数（Area Fraction）回归 |
| `07c_exercises.ipynb` | 第七讲基础巩固习题（8 道独立小练习：张量操作、Autograd 多元求导、MLP 参数量手算、自定义 `nn.Module`、手写回归训练循环、MC Dropout 均值与标准差、二维卷积核响应与输出尺寸、轻量级微结构 CNN 搭建） |
| `solutions/07_nn_solutions.ipynb` | `07a` 与 `07b` 全部随堂练习（`07a-1` 至 `07b-3`）的完整参考代码与解析 |
| `solutions/07_exercises_solutions.ipynb` | `07c_exercises.ipynb` 8 道基础巩固习题的完整参考答案 |

## 建议学习顺序

建议按 `07a` $\to$ `07b` $\to$ `07c_exercises` 的顺序阅读与运行，全部代码均针对 CPU 环境做过轻量化设计，单本 notebook 运行时间在 1–2 分钟以内。
