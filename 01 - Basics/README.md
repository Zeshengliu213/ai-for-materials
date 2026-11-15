# 第一部分：Python 与化学/材料数据基础

本模块面向零编程基础的材料与化学专业研究生，通过四个循序渐进的实战 Notebook，完成从 Python 基础语法、表格清洗、科研绘图到 RDKit 分子特征表示的完整入门。

| Notebook | 核心内容 |
|---|---|
| `01a_python_crash_course.ipynb` | Jupyter/Colab 操作，变量与算术运算，字符串与 f-string，列表/元组/字典，条件判断，循环与列表推导式，函数封装，`import` 与 NumPy 向量化初探，常见报错排查 |
| `01b_pandas.ipynb` | 纯 Python 文本读写；Pandas `DataFrame`/`Series` 入门，读入 AqSolDB，数据体检，选列选行与多条件筛选，排序，列运算与 `.apply()`，`groupby` 分组统计，`merge`/`concat` 与缺失值处理 |
| `01c_plotting.ipynb` | Matplotlib 折线图、经验公式拟合与外推风险、直方图、多维散点图、多子图排版与高清导出；Seaborn 分组分布、箱线图、回归趋势、相关性热图与 `pairplot` |
| `01d_rdkit_basics.ipynb` | SMILES 语法、分子绘制与规范化（Canonical SMILES），原子/键/共轭/环系遍历，物理化学描述符，Morgan 指纹与 Tanimoto 相似度，Murcko 骨架，RDKit + Pandas 批量清洗与 SMARTS 子结构检索 |
| `01e_exercises.ipynb` | **第一讲基础巩固习题**：涵盖 Python 语法、NumPy/Pandas 数据筛选统计、Matplotlib 双子图绘制与 RDKit 描述符/指纹计算的 10 道分步基础练习 |
| `solutions/01_basics_solutions.ipynb` | `01a`–`01d` 全部 13 道随堂练习的参考答案与解析 |
| `solutions/01_exercises_solutions.ipynb` | `01e_exercises.ipynb` 全部 10 道基础习题的参考答案与解析 |
| `data/solubility.csv` | AqSolDB 水溶解度数据集（9482 个化合物的名称、SMILES、实验 $\log S$ 及 17 个 RDKit 描述符） |

建议学习顺序：`01a` → `01b` → `01c` → `01d`，每个 Notebook 约需 1.5 至 2 学时。

## 教学主线与核心伏笔

- **领域背景主线**：以**有机光电材料（有机半导体）**贯穿始终（并苯系列、噻吩/P3HT、BTBT/C8-BTBT、TIPS-并五苯、红荧烯、苝/PTCDA、咔唑、三苯胺）。四个 Notebook 围绕同一个物理化学问题展开：*大 $\pi$ 共轭核赋予材料优异的电荷传输性能，但也导致分子间强烈堆积而极难溶解；因此必须在共轭核上引入柔性侧链以兼顾溶液加工性。* 学生会在 `01b`（按芳香环数 `groupby`）、`01c`（箱线图与多维散点图）、`01d`（Murcko 骨架剥离与蒽核子结构搜索：含蒽核分子平均 $\log S$ 低约 4 个单位，即溶解度低约 1 万倍）中三次从不同维度验证这一规律。
- **为后续机器学习章节埋下的关键伏笔**：
  - `01c`：用 $E_{\text{gap}} = a + b/N$ 拟合光学能隙，引出经验模型在训练区间之外**外推（Extrapolation）**的失效风险；
  - `01c`：通过相关性热图观察 `MolWt` 与 `RingCount`（$r \approx 0.62$）、`TPSA` 与 `NumHAcceptors`（$r \approx 0.87$）之间的**多重共线性**；
  - `01d`：通过 **Canonical SMILES** 强调多源数据去重与防止训练集/测试集**数据泄漏（Data Leakage）**，通过 **Murcko 骨架**引出 **Scaffold Split（骨架划分）**；
  - `01d`：发现二值 Morgan 指纹（$r=2$）无法区分并四苯与并五苯（Tanimoto 相似度 = 1.0），直观揭示“**分子特征表示决定了模型的上限**”；
  - `01d`：在真实数据集中排查出 2 条无法解析的错误 SMILES 以及 1044 条含 `.` 的盐/多组分记录，培养在建模前先做数据清洗的习惯。

## 运行环境与验证说明

- **本地环境**：Python ≥ 3.8，需安装 `numpy pandas matplotlib seaborn rdkit jupyter`。
- **Google Colab**：`01a`–`01c` 无需额外安装；`01d` 第一格代码会自动检测并安装 `rdkit`；若未找到本地 `data/solubility.csv`，会自动弹出文件上传控件。
- **注意事项**：
  - `01a` 第 9 节包含 3 个故意写错的演示代码格（已标记 `raises-exception`），运行时抛出异常属于正常教学设计。
  - `01a` 与 `01c` 中引用的能隙、HOMO/LUMO 及迁移率数值均为教学示意近似值，请勿作为文献标准值引用。
