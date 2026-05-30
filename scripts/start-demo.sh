#!/usr/bin/env bash
# 一键启动答辩演示环境：docker + ngrok + caffeinate
# 用法：./scripts/start-demo.sh
# 停止：./scripts/stop-demo.sh

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "→ 1/4 检查 Docker daemon"
if ! docker info >/dev/null 2>&1; then
  echo "   Docker 没启动，正在打开 Docker Desktop…"
  open -a Docker
  echo -n "   等待 daemon 就绪"
  until docker info >/dev/null 2>&1; do
    sleep 2
    echo -n "."
  done
  echo " ✓"
else
  echo "   Docker 已运行 ✓"
fi

echo "→ 2/4 启动 docker compose（prod）"
docker compose -f docker-compose.prod.yml up -d
sleep 3
echo "   本地访问：http://localhost"

echo "→ 3/4 启动 caffeinate（防睡眠，后台）"
if pgrep -x caffeinate >/dev/null; then
  echo "   caffeinate 已在跑 ✓"
else
  nohup caffeinate -di >/dev/null 2>&1 &
  echo "   已启动 (PID $!) ✓"
fi

echo "→ 4/4 启动 ngrok（公网链接）"
echo "──────────────────────────────────────────────────────────"
echo "本地链接：http://localhost"
echo "公网链接：见下方 ngrok Forwarding URL（你账号绑定的固定 *.ngrok-free.dev 子域名）"
echo "──────────────────────────────────────────────────────────"
echo "ngrok 输出如下（这个终端不能关，关了公网链接就失效）："
echo ""

# 清掉代理，ngrok 不允许走代理
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
exec ngrok http 80
