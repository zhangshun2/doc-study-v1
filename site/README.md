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
- `_site/assets/app.js`、`app.css`：阅读站点界面。

`site/assets/vendor/` 保存固定版本的浏览器依赖，避免运行时依赖外部 CDN。

## 发布方式

推送 `master` 或 `main` 后，GitHub Actions 会执行 `python3 site/build.py`，再把 `_site` 部署到 GitHub Pages。

GitHub 仓库需要把 `Settings -> Pages -> Build and deployment -> Source` 设为 `GitHub Actions`。工作流已开启自动配置，但首次发布后仍应在仓库设置中确认这一项。
