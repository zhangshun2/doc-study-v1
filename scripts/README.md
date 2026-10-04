# 发布脚本与规则

目标：本地只有一份内容，一次提交同时落到 Gitee 和 GitHub，并让 GitHub 自动重建站点。

## 仓库与分支约定

| 远端 | 地址 | 发布分支 | 说明 |
| --- | --- | --- | --- |
| `origin` | `git@gitee.com:zhangdatou/doc-study-v1.git` | `master` | 主仓库，日常备份与国内访问 |
| `github` | `git@github.com:zhangshun2/doc-study-v1.git` | `main` | GitHub 默认分支，触发 Pages 构建 |

本地只有一个长期分支 `master`。GitHub 上没有 `master`，发布时把本地的 `master` 推成那边的 `main`，两边内容始终一致。

其他分支（如 `develop`、旧 `master-docsify`）不属于发布分支，脚本不会动它们。

## 脚本

| 脚本 | 用途 |
| --- | --- |
| `scripts/publish.sh` | 一条命令发布到两个仓库，并等待 GitHub 构建结果 |
| `scripts/preview.sh` | 本地构建并起预览服务，发布前自查 |
| `scripts/install-hooks.sh` | 启用 `pre-push` 钩子（新克隆仓库跑一次） |

### 日常发布

```bash
scripts/publish.sh
```

它会依次做四件事：

1. 检查工作区是否干净、当前是否在 `master`。
2. 本地跑一次 `python3 site/build.py`，构建失败就不发布。
3. 推送 `origin/master` 与 `github/main`。
4. 通过 GitHub API 确认这次提交已经触发构建，并打印运行页和站点地址。

可调环境变量：`WAIT_SECONDS=0` 跳过构建状态检查，`SKIP_BUILD=1` 跳过本地构建自检。

### 直接用 git push

习惯直接敲 git 命令时，用 `git push origin master` 也一样：`pre-push` 钩子会把同一次提交镜像到 GitHub 的 `main`，并打印同步结果。反向推送 `git push github master:main` 时也会镜像回 Gitee。

钩子只是兜底，失败时不会阻断你原本的 push，会提示改用 `scripts/publish.sh` 补发。

### 发布前预览

```bash
scripts/preview.sh          # 默认 http://127.0.0.1:4173/
PORT=5000 scripts/preview.sh
```

## 规则

- 正文只改 `学习文库/算法学习`，不要为了发布复制第二份 Markdown。
- 不在 `master` 上直接堆半成品：要么提交完整改动，要么先建临时分支。
- 发布前必须能通过 `python3 site/build.py`；`_site/` 是构建产物，永远不提交。
- 两个仓库的内容以同一次提交为准，出现分叉时先 `git fetch` 看差异，不要强推。
- 站点上线由 GitHub Actions 完成，不用手工上传 `_site`。

## GitHub 自动构建

`.github/workflows/pages.yml` 在 `master` 或 `main` 有推送时自动执行：构建站点、上传产物、发布到 GitHub Pages，站点地址 <https://zhangshun2.github.io/doc-study-v1/>。

仓库需要保持两项设置开启（管理员权限，只能在网页操作）：

1. `Settings -> Actions -> General`：允许运行 Actions。
2. `Settings -> Pages -> Build and deployment -> Source`：选择 `GitHub Actions`。
