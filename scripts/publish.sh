#!/usr/bin/env bash
# 把本地 master 一次发布到两个仓库，并等待 GitHub 的自动构建结果。
set -euo pipefail

GITEE_REMOTE="${GITEE_REMOTE:-origin}"
GITHUB_REMOTE="${GITHUB_REMOTE:-github}"
BRANCH="${BRANCH:-master}"
GITHUB_BRANCH="${GITHUB_BRANCH:-main}"
WAIT_SECONDS="${WAIT_SECONDS:-90}"
SKIP_BUILD="${SKIP_BUILD:-0}"

cd "$(git rev-parse --show-toplevel)"

info() { printf '\033[36m[publish]\033[0m %s\n' "$1"; }
fail() { printf '\033[31m[publish]\033[0m %s\n' "$1" >&2; exit 1; }

# 1. 工作区必须干净，避免发出半成品
if ! git diff --quiet || ! git diff --cached --quiet; then
  fail "工作区有未提交改动，先提交再发布"
fi
if [ -n "$(git ls-files --others --exclude-standard)" ]; then
  info "提示：存在未跟踪文件，已忽略（不会进入本次提交）"
fi

# 2. 只从约定分支发布
current="$(git rev-parse --abbrev-ref HEAD)"
[ "$current" = "$BRANCH" ] || fail "当前分支是 $current，发布需要 $BRANCH"

# 3. 本地构建自检，保证 Actions 里跑的是能构建的提交
if [ "$SKIP_BUILD" != "1" ]; then
  info "本地构建自检"
  python3 site/build.py
  python3 -m json.tool _site/assets/manifest.json >/dev/null
fi

sha="$(git rev-parse HEAD)"
info "发布提交 ${sha:0:7}：$GITEE_REMOTE/$BRANCH 与 $GITHUB_REMOTE/$GITHUB_BRANCH"

# 4. 推送到 Gitee
git push "$GITEE_REMOTE" "$BRANCH:$BRANCH"

# 5. 推送到 GitHub 默认分支
git push "$GITHUB_REMOTE" "$BRANCH:$GITHUB_BRANCH"

# 6. 确认 GitHub Actions 已被推送触发
slug="$(git config --get "remote.$GITHUB_REMOTE.url" \
  | sed -E 's#^git@github\.com:##; s#^https://github\.com/##; s#\.git$##')"

if [ "$WAIT_SECONDS" = "0" ]; then
  info "已跳过构建状态检查"
  exit 0
fi

info "等待 GitHub Actions 接单（最多 ${WAIT_SECONDS}s）"
deadline=$(( $(date +%s) + WAIT_SECONDS ))
run_url=""
while [ "$(date +%s)" -lt "$deadline" ]; do
  run_url="$(curl -fsS --max-time 15 \
    "https://api.github.com/repos/$slug/actions/runs?head_sha=$sha&per_page=1" \
    | python3 -c 'import json,sys;d=json.load(sys.stdin);r=d.get("workflow_runs") or [];print(r[0]["html_url"] if r else "")' \
    2>/dev/null || true)"
  [ -n "$run_url" ] && break
  sleep 6
done

if [ -z "$run_url" ]; then
  info "暂未查到运行记录，去 Actions 页确认：https://github.com/$slug/actions"
else
  info "构建已触发：$run_url"
  info "站点地址：https://${slug%%/*}.github.io/${slug##*/}/"
fi
