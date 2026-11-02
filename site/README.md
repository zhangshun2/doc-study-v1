# 学习站说明

源码仍只维护在 `学习文库/算法学习`。`site/` 只负责把现有 Markdown 构建成可浏览、可搜索的学习网站，不会改写 Obsidian 正文。

## 本地构建

```bash
python3 site/build.py
python3 -m http.server 8000 -d _site
```

打开 `http://localhost:8000`。

## 构建产物

- `_site/content/`：从正式算法库复制的 Markdown 和辅助文件。
- `_site/assets/manifest.json`：导航、统计、文档属性与复习状态。
- `_site/assets/search.json`：按需加载的全文检索索引。
- `_site/assets/fact-bank.json`：从 `学习文库/算法学习/problems.json` 构建的官方题面事实快照。
- `_site/assets/app.js`、`app.css`：阅读站点界面。

`site/assets/vendor/` 保存固定版本的浏览器依赖，避免运行时依赖外部 CDN。

## 官方事实题库

`学习文库/算法学习/problems.json` 是官方题面、约束、示例、提示和 Java 签名的唯一事实源。`fact-bank.json` 只是构建产物，不在 Markdown 里手抄第二份题面，避免原文和笔记页面对不上。

首页的“官方事实题库”入口按四种正交方式浏览：

- `官方事实`：直接投影题面快照，按 LeetCode 难度排列。
- `面试高频`：本地清单中标记为 P0 的策展视图，不是 LeetCode 官方评级。
- `体系形态`：按问题本身的计算形态重排，一道题只归入一个主要形态。
- `官方标签`：保留 LeetCode 标签，用于原样检索；标签不证明某个算法方向。

题目详情先呈现原题事实、约束、示例和复杂度要求。签名与 Java 模板默认收起，必须先完成自己的读题、对象过程、范围分析和方向确认，再打开代码。题解链接指向正式文档中的推导、答案和代码锚点，不另存一套答案。

## 发布方式

推送 `master` 或 `main` 后，GitHub Actions 会执行 `python3 site/build.py`，再把 `_site` 部署到 GitHub Pages。

GitHub 仓库需要把 `Settings -> Pages -> Build and deployment -> Source` 设为 `GitHub Actions`。工作流已开启自动配置，但首次发布后仍应在仓库设置中确认这一项。

预期地址：<https://zhangshun2.github.io/doc-study-v1/>

### 首次发布排查

如果推送后 `https://github.com/zhangshun2/doc-study-v1/actions` 里一直没有运行记录，说明仓库还未启用 Actions，需要在 GitHub 页面手动开启：

1. `Settings -> Actions -> General`，把 `Actions permissions` 设为允许运行。
2. `Settings -> Pages -> Build and deployment -> Source` 选择 `GitHub Actions`。
3. 打开 `Actions` 页中的 `Deploy GitHub Pages`，点击 `Run workflow` 触发一次。

两处设置属于仓库管理员权限，只能在 GitHub 网页操作，无法由本地脚本代替。

## 日常维护

1. 只在 `学习文库/算法学习` 里编辑 Markdown 与属性，站点不保存第二份正文。
2. 新增或修改后本地运行 `python3 site/build.py` 预览，确认导航、搜索与双链都正常。
3. 提交并推送到 Gitee `origin` 与 GitHub `github`；GitHub 收到推送后自动重建并发布。

只有修改 `site/` 下的构建器、前端或样式时才需要动代码；改题目内容不需要碰 `site/`。
