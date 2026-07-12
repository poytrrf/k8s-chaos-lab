#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> 检查 minikube 状态"
if ! minikube status >/dev/null 2>&1; then
  echo "==> 启动 minikube"
  minikube start --cpus=4 --memory=6g --driver=docker
  minikube addons enable metrics-server
fi

echo "==> 切换到 minikube 的 docker daemon (本地构建镜像直接可用，不用 push 到远程仓库)"
eval "$(minikube docker-env)"

echo "==> 构建 service-a 镜像"
docker build -t service-a:latest "$PROJECT_ROOT/app/service-a"

echo "==> 构建 service-b 镜像"
docker build -t service-b:latest "$PROJECT_ROOT/app/service-b"

echo "==> 应用 k8s 配置"
kubectl apply -f "$PROJECT_ROOT/k8s/base/"

echo "==> 等待所有 Pod 就绪"
kubectl -n chaos-lab wait --for=condition=Ready pods --all --timeout=180s || true

echo "==> 当前状态"
kubectl -n chaos-lab get pods,svc

echo ""
echo "==> 访问方式:"
echo "    minikube service nginx-gateway -n chaos-lab --url"
