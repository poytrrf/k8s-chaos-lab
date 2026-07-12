# K8s 故障注入与自愈演练项目

一个本地 Kubernetes 环境下的服务可靠性实践项目：从基础部署 -> 监控告警 -> 故障注入 -> 自愈优化的完整闭环。

## 项目状态
🚧 开发中，进度见下方 Day 计划。

## 架构

（Day 15 补充架构图）

## 技术栈
- Kubernetes: minikube
- 网关: Nginx (Ingress / 或 Nginx 反向代理 Deployment)
- 后端: service-a, service-b (Python Flask)
- 存储: PostgreSQL, Redis
- 监控: Prometheus + Grafana
- 告警: Alertmanager

## 目录结构
```
k8s-chaos-project/
├── app/                # 后端服务源码
│   ├── service-a/
│   └── service-b/
├── k8s/
│   ├── base/           # 基础服务部署配置
│   └── monitoring/     # Prometheus/Grafana/Alertmanager配置
└── docs/                # 故障场景记录、排查手册
```

## 故障场景表格
（Day 9-11 补充）

## 排查手册
（Day 9-11 补充）
