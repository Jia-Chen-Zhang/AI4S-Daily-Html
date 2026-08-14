#!/usr/bin/env bash
# 一键发布:导出最新报告数据 → 提交 → 推送到 GitHub(触发 Pages 重新部署)
# 用法: ./scripts/publish.sh "可选的提交说明"
set -euo pipefail

GITWEB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$GITWEB_DIR"

echo "📤 导出最新报告数据..."
# 优先用主仓库的 venv(有 pyyaml),否则回退系统 python3
if [[ -x "../.venv/bin/python" ]]; then
    ../.venv/bin/python scripts/export.py
else
    python3 scripts/export.py
fi

echo "📦 提交并推送..."
git add public/data
if git diff --cached --quiet; then
    echo "ℹ️ 数据无变化,跳过提交"
    exit 0
fi
git commit -m "${1:-数据更新 $(date +%Y-%m-%d)}"
git push
echo "✅ 已推送,GitHub Actions 将自动重新部署 Pages(约 1-2 分钟)"
