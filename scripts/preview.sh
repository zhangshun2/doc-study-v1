#!/usr/bin/env bash
# 本地构建并预览学习站，用来在发布前检查导航、搜索和样式。
set -euo pipefail

PORT="${PORT:-4173}"

cd "$(git rev-parse --show-toplevel)"

python3 site/build.py
python3 -m json.tool _site/assets/manifest.json >/dev/null

printf '\033[36m[preview]\033[0m http://127.0.0.1:%s/\n' "$PORT"
printf '\033[36m[preview]\033[0m Ctrl+C 结束预览\n'
exec python3 -m http.server "$PORT" -d _site
