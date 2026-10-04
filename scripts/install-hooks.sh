#!/usr/bin/env bash
# 启用仓库内的 Git 钩子（新克隆的仓库需要跑一次）。
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

chmod +x .githooks/pre-push scripts/*.sh
git config core.hooksPath .githooks

printf '\033[36m[hooks]\033[0m 已启用 %s 下的钩子\n' ".githooks"
printf '\033[36m[hooks]\033[0m pre-push：推送 master 时自动镜像到另一个仓库\n'
