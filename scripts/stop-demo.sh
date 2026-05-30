#!/usr/bin/env bash
# 停止答辩演示环境
# 用法：./scripts/stop-demo.sh

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "→ 停 ngrok"
pkill -f "^ngrok " 2>/dev/null && echo "   ngrok 已停 ✓" || echo "   ngrok 没在跑"

echo "→ 停 caffeinate"
pkill -x caffeinate 2>/dev/null && echo "   caffeinate 已停 ✓" || echo "   caffeinate 没在跑"

echo "→ 关 docker compose"
docker compose -f docker-compose.prod.yml down

echo ""
echo "全部关掉了。Qdrant 数据保留在 volume 里，下次启动直接 ./scripts/start-demo.sh"
