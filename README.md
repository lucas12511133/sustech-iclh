# SUSTech ICLH · 生命科学与大健康创新中心

南方科技大学生命科学学院“生命科学与大健康创新中心”专题网页，包含完整中英文版本。静态 HTML、CSS、JavaScript 实现，无需安装前端依赖或执行构建。

A bilingual website for the Innovative Center for Life Science and Health at SUSTech School of Life Sciences. Built with static HTML, CSS and JavaScript.

## 在线访问 / Website

- 中文：https://lucas12511133.github.io/sustech-iclh/
- English: https://lucas12511133.github.io/sustech-iclh/en.html

GitHub Actions 会在 `main` 分支更新后检查并自动部署 `dist/`。源码仓库保持私有，GitHub Pages 网页公开访问。

## 本地预览 / Local preview

在仓库根目录运行：

```sh
python -m http.server 4174 --directory dist
```

- 中文：`http://localhost:4174/index.html`
- English: `http://localhost:4174/en.html`
- 顶部 `EN / 中文` 切换语言，并保留当前浏览板块。
- `?lang=en-us` 兼容入口自动转至英文版。

## 功能 / Features

- 单页长页面、固定页内导航和手机端适配。
- 四分环形中心职能图，支持点击及键盘切换。
- 两位教授照片链接至各自的官方主页。
- 项目介绍支持展开，研究示意图支持放大。
- 学院官网青蓝色主题 `#18BFC5`。
- 中文字体栈沿用学院中文版官网，英文使用 Exo 2。

## 文件结构 / Structure

```text
dist/
  index.html             中文页面
  en.html                English page
  styles.css             共享布局及交互样式
  typography.css         中文字体及文字层级
  english.css            English typography and layout
  script.js              页面交互与语言切换
  assets/                图片、字体和研究示意图
build-english.py          中英翻译字典及英文页面生成脚本
build-english-figures.py  英文研究示意图生成脚本
check.cjs                 双语页面的本地资源、锚点和翻译完整性检查
```

## 更新与检查 / Maintenance

编辑 `dist/index.html` 后，同步维护 `build-english.py` 内的英文翻译，再运行：

```sh
python build-english.py
python build-english-figures.py
node check.cjs
node --check dist/script.js
```

两个 Python 脚本仅使用标准库。上述 Node.js 命令也无需 npm 依赖。

## 官网接入 / Integration

将 `dist/` 内文件整体上传至学院官网指定目录，并从“科学研究 / 科研创新平台”链接到本页面。也可在接入学院 CMS 时替换统一页头和页脚。联系邮箱目前使用已标明的学院公开邮箱。

## 素材来源 / Sources

- 中心介绍、人物、课堂、合作及项目素材：用户提供的《创新中心海报(2).pptx》。
- 当前首屏湖景照片：用户提供的南科大校园照片；网页采用 WebP 版本，原照片内容与水印保留。
- 学院标识、配色与字体参考：[南方科技大学生命科学学院](https://bio.sustech.edu.cn/)。
- 字体文件：[学院官网 Exo 2](https://bio.sustech.edu.cn/static/site/font/Exo2-Regular.ttf)。
- 校园图库素材：[南科视界](https://www.sustech.edu.cn/zh/gallery.html)。
- 英文研究示意图：依据中心提供的项目介绍整理，分别用于 LLPS 支架蛋白设计和 AI 驱动的 RNA 药物研发。

