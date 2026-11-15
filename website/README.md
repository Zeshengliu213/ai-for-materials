# AI for Materials Science 课程网站使用与更新指南

本目录是课程仓库的子目录（仓库根目录即课程内容）。它把仓库根下的所有教学大纲、`README.md`、`.ipynb` 互动课件、`solutions/` 参考答案、`data/` 数据集与 `slides/` 讲课幻灯片自动构建为学术风格的公开静态网站。

## 1. 安装构建依赖（只需一次）

Markdown、数学公式与代码高亮全部在**构建时**渲染，因此构建脚本需要两个 Python 库：

```bash
pip install -r website/requirements.txt
```

## 2. 构建与本地预览

```bash
python website/build.py
```

脚本会扫描全部模块并重新生成 `website/dist/` 中的所有页面。`dist/files/`（数据集与课件下载）和 `dist/slides/` 按内容哈希存储，内容没变就原样保留、不重复拷贝，构建日志会显示复用了多少体积；源文件删除后对应的残留文件会被自动清理。需要从零重建时加 `--clean`：

```bash
python website/build.py --clean
```

预览方式：

- **直接打开**：双击 `website/dist/index.html`。所有页面使用相对路径，KaTeX 已本地化到 `assets/vendor/`，因此离线 `file://` 打开也能正常显示公式、代码高亮与全站搜索。
- **本地静态服务器**（推荐）：

  ```bash
  python -m http.server 8010 --directory website/dist
  ```

  然后访问 `http://localhost:8010`。

## 3. 如何更新课件内容

只需维护 `course/` 文件夹，然后重新构建：

1. 在章节目录（如 `course/04 - Bayesian Optimization/`）中添加或更新 `.ipynb` 课件、`README.md`、`data/` 数据集或 `solutions/` 答案。
2. 把讲课幻灯片放到 `course/slides/<模块号+字母>/index.html`（例如 `course/slides/01a/index.html`）。目录名以两位模块号开头即可被自动识别并挂到对应模块页面。
3. 运行 `python website/build.py`。

### 新增模块的元信息

模块标题、学期归属、完成状态与「编写计划」大纲写在 `website/builder/config.py` 的 `MODULE_META` 中。尚未编写的模块可以在 `outline` 里列出计划条目，网站会在模块页与首页卡片上展示，而不是显示一句空洞的“持续完善中”。

### 习题与参考答案的识别规则

文件名里含 `exercises` 的 Notebook（如 `01e_exercises.ipynb`、`solutions/01_exercises_solutions.ipynb`）
会被自动识别为**习题**，并与讲解课件分开展示：

- 模块页分成「互动实战课件 / 课后习题 / 参考答案」三块，习题行带「参考答案」直达按钮；
- 全站多出一个 `exercises.html` 习题汇总页（顶栏「习题与答案」），按模块列出全部习题；
- 还没有习题的模块，在汇总页上会显示一句提示，而不是直接消失。

新增习题时**不需要改任何代码**，按命名规则放进模块目录并重新构建即可。

### 开启 Colab 一键打开

已配置为课程仓库 `Zeshengliu213/ai-for-materials`（`website/builder/config.py`）：

```python
GITHUB_REPO = "Zeshengliu213/ai-for-materials"
GITHUB_BRANCH = "main"
GITHUB_COURSE_PREFIX = ""   # course/ 目录本身就是仓库根目录
```

每份 Notebook 页面、模块表格与习题汇总页都会出现「▶ 在 Colab 中打开」按钮，学生无需下载再上传。

> **注意**：Colab 是从 GitHub **远端** 读取文件的。本地新增或修改的 Notebook
> 必须 `git push` 到 `main` 之后，对应的 Colab 链接才不会 404。

### 配置站点网址（SEO 与分享卡片）

站点网址有三种设置方式（优先级从高到低）：

```bash
python website/build.py --base-url https://你的域名      # 构建时指定（推荐，部署脚本里写一行即可）
AI4M_BASE_URL=https://你的域名 python website/build.py   # 环境变量
```

或直接在 `config.py` 里写死 `SITE_BASE_URL = "https://你的域名"`。

设置之后构建会额外产出：`sitemap.xml`（并在 `robots.txt` 中引用）、**每页独立**的
`canonical` 与 `og:url`，以及指向 `assets/social-card.svg` 的大图分享卡片
（`twitter:card: summary_large_image`）。不设置则这些标签全部跳过，构建日志会提醒一次。

## 4. 公开部署到互联网（免费方案）

生成的是纯静态网站（`website/dist/`），无需后端服务器：

- **Netlify / Vercel / Cloudflare Pages**：
  - 直接把 `website/dist` 拖拽上传到 Netlify Drop / Cloudflare Pages 即可获得公开网址。
  - 绑定 GitHub 仓库时，构建命令设为 `pip install -r website/requirements.txt && python website/build.py`，发布目录设为 `website/dist`。
- **GitHub Pages（本仓库当前方案）**：`.github/workflows/pages.yml` 已配置好——
  推送到 `main` 即自动安装依赖、构建并发布 `website/dist`，站点网址由工作流
  按 `https://<owner>.github.io/<repo>` 自动推导后传给 `--base-url`，无需手工改配置。

  > **首次使用需手动开一次开关**：仓库 Settings → Pages → Build and deployment →
  > Source 选择 **GitHub Actions**。只需设置一次，之后每次推送自动部署。

  `website/dist/` 已加入 `.gitignore`：产物由 Actions 构建，不进版本库。

## 5. 目录结构

```
website/
├── build.py              # 构建入口（检查依赖 → 清理产物 → 扫描 → 生成）
├── requirements.txt      # 构建依赖
├── builder/
│   ├── config.py         # 站点与模块元信息、Colab/SEO 开关
│   ├── collect.py        # 扫描 course/、数据集哈希去重、幻灯片识别、阅读顺序
│   ├── rendering.py      # 构建时 Markdown + 数学公式 + Pygments 高亮（含暗色）
│   ├── notebooks.py      # .ipynb → HTML（含目录抽取与输出渲染）
│   ├── templating.py     # Jinja2 环境与各模板共用的上下文
│   └── pages.py          # 首页、模块页、课件页、答案页、搜索索引、sitemap
├── templates/            # 所有 HTML 模板（Jinja2）
│   ├── thumbs/           # 模块缩略图与路线图图标（内联 SVG，随主题变色）
│   ├── _roadmap.html     # 首页课程知识脉络路线图
│   ├── base.html         # 文档骨架：head、顶栏、搜索框、主题开关、页脚
│   ├── doc_base.html     # 侧边栏 + 正文 + 右侧目录的三栏布局
│   ├── index.html / module.html / notebook.html / solution.html
│   ├── exercises.html    # 全部习题与参考答案汇总页
│   └── _sidebar.html / _toc.html / _pager.html / _module_card.html
├── tools/
│   └── build_fonts.py    # 生成中文衬线字体子集（手动运行，产物已提交）
├── assets/
│   ├── style.css         # 基础样式与浅色主题变量
│   ├── components.css    # 搜索、目录、翻页、答案遮挡、暗色主题
│   ├── app.js            # KaTeX 渲染、全站搜索、目录高亮、答案展开、学习进度、主题切换
│   ├── social-card.svg   # 社交分享大图（需设置站点网址后才会被引用）
│   ├── fonts/            # Noto Serif SC 子集（约 520 KB）与 fonts.css
│   └── vendor/katex/     # 本地化的 KaTeX（含 woff2 字体）
└── dist/                 # 构建产物（勿手工编辑）
```

## 6. 视觉系统：缩略图与知识脉络图

### 科研示意图的配色写法

`templates/thumbs/` 下的 SVG **不写任何十六进制颜色**，只用 `components.css` 里定义的
`.vz-*` 类（`vz-line` / `vz-axis` / `vz-fill-navy` / `vz-band` / `vz-token` …）。
这些类全部引用站点的设计变量，因此深浅色主题自动切换——暗色下用的是
`--accent-navy-light`（亮蓝）而不是 `--accent-navy`（近黑），不会糊成一团。
箭头标记 `url(#vz-arrow)` 由 `base.html` 顶部的一个全局 `<defs>` 提供，每页只定义一次。

### 模块缩略图

每个模块一张 `templates/thumbs/<模块号>.svg`（viewBox `0 0 320 110`），在首页卡片顶部
内联展开，内容对应该模块的代表性图形：01 数据表→分子、02 parity plot、03 化学空间聚类、
04 GPR 置信带、05 SHAP 蜂群、06 晶胞+XRD、07 CNN+全连接层、08 注意力弧、09 隐空间采样、
10 消息传递图。新增模块时放一张同名 SVG 即可，缺失时模板用 `ignore missing` 静默跳过。
`todo` 状态的模块缩略图会自动降饱和度。

### 首页知识脉络路线图

路线图的分段写在 `config.py` 的 `ROADMAP_STAGES` 里（只写模块号），构建时与
`MODULE_META` 合并，因此标题、状态颜色永远和大纲一致，不会写死后失同步。
每个节点是一张卡片 + 一枚 48×48 图标（`thumbs/stage-N.svg`），模块小标签直接链到模块页。
桌面端固定 3 列（6 段 → 3×2），列与列之间用 CSS 箭头连接，换行处自动隐藏箭头；
窄屏降为 2 列 / 1 列并去掉箭头。

## 7. 主题与字体

- **暗色模式**：顶栏右侧的 ☀/☾ 按钮可切换，选择保存在 `localStorage`；未手动选择时跟随系统 `prefers-color-scheme`。主题在首屏绘制前由 `base.html` 中的内联脚本确定，不会闪白。代码高亮有独立的暗色配色；Notebook 中的 matplotlib 图像在暗色下会加白色衬底，保证坐标轴可读。
- **中文衬线字体**：标题使用 Noto Serif SC。完整 CJK 字体有 22 MB，因此 `tools/build_fonts.py` 会扫描 `course/` 下所有 README 与 Notebook 的 Markdown，只保留实际用到的字符（当前约 1600 个），生成约 520 KB 的可变字重 woff2。产物已提交，**日常构建不需要联网，也不需要 fontTools**。只有当新增内容引入了全新汉字时才需要重新生成：

  ```bash
  pip install fonttools brotli
  python website/tools/build_fonts.py
  ```

## 8. 实现要点

- **零 CDN 依赖**：KaTeX 已本地化，Markdown 与代码高亮在构建时完成，断网或 CDN 不可用时站点依然完整可读，搜索引擎也能抓到正文。
- **数据集去重**：相同内容的文件（如被 7 个模块共用的 2.2 MB `solubility.csv`）按 SHA-256 只存一份于 `dist/files/_shared/`，下载链接通过 `download` 属性保留原始文件名。构建日志会打印节省的体积。
- **全站搜索**：构建时生成 `dist/assets/search-index.js`（以 JS 而非 JSON 输出，这样 `file://` 下也能用），顶栏搜索框支持标题与正文匹配，按 `/` 聚焦。
- **答案遮挡**：答案页默认折叠，点击确认后展开，并在当前标签页内记住选择（关闭标签页后重新折叠）。
- **学习进度**：课件页顶部与底部有「标记为已学完」按钮，模块页与习题汇总页每行有勾选框，
  首页有总进度条与「重置进度」。记录存在浏览器 `localStorage` 的 `ai4m-progress`
  （`{页面href: 1}`），不上传服务器；同一浏览器的多个标签页通过 `storage` 事件实时同步。
  所有进度界面都由 `data-progress-keys` / `data-progress-key` 属性驱动，加新页面不用改 JS。
- **顺序阅读**：每个模块页与课件页底部提供「上一讲 / 下一讲」，顺序为模块 → 该模块的各个 Notebook。
- **模板与逻辑分离**：HTML 全部在 `templates/`，`builder/pages.py` 只负责准备上下文。改版式不必碰 Python；模板开启了 `autoescape` 与 `StrictUndefined`，拼错变量名会在构建时直接报错而不是静默输出空白。
- **SEO**：每页带 `description`、独立 `canonical` 与 Open Graph 标签，首页额外输出 Schema.org `Course` 结构化数据；填好站点网址后会生成 `sitemap.xml` 与分享大图卡片。
