# Deployment Guide

## Prerequisites
- Docker Desktop installed
- kubectl installed
- Helm installed
- Minikube installed
- Python 3.11+
- Git and GitHub account

## Step 1 - Clone the Repository
```bash
git clone https://github.com/Abdell001/ai-platform.git
cd ai-platform
```

## Step 2 - Start Minikube
```bash
minikube start --driver=docker --cpus=4 --memory=4096
```

## Step 3 - Install Monitoring Stack
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
helm install loki grafana/loki-stack -n monitoring
```

## Step 4 - Deploy the Application
```bash
helm install ai-platform ./helm/ai-platform
```

## Step 5 - Verify Deployment
```bash
kubectl get pods        # all pods Running
kubectl get svc         # services created
kubectl get hpa         # autoscaler active
```

## Step 6 - Install Vault
```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault hashicorp/vault -n vault --create-namespace
kubectl exec -n vault vault-0 -- vault operator init -key-shares=1 -key-threshold=1
kubectl exec -n vault vault-0 -- vault operator unseal <UNSEAL_KEY>
```

## Step 7 - Test the Application
```bash
kubectl port-forward svc/ai-api 8080:8000
curl http://localhost:8080/health
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is DevOps?", "session_id": "test1"}'
```

## Verify Successful Deployment
- All pods show Running status
- /health returns {"status": "healthy"}
- /chat returns AI-generated response
- Grafana dashboards show metrics at localhost:3000
