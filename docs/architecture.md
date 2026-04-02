# AI Platform Architecture

## System Overview
A production-grade AI platform for customer support, built on Kubernetes.

## Services
| Service    | Technology        | Purpose                        |
|------------|-------------------|--------------------------------|
| API        | FastAPI (Python)  | Gateway between users and AI   |
| LLM        | Ollama + Mistral  | AI response generation         |
| Cache      | Redis             | Response caching               |
| Database   | PostgreSQL        | Conversation history           |
| Monitoring | Prometheus+Grafana| Metrics and dashboards         |
| Logs       | Loki + Promtail   | Log aggregation                |
| Secrets    | HashiCorp Vault   | Secrets management             |
| CI/CD      | GitHub Actions    | Automated build and deploy     |
| GitOps     | ArgoCD            | Kubernetes deployment sync     |

## Layers
- **Application Layer**: FastAPI, Ollama, Redis, PostgreSQL
- **Orchestration Layer**: Kubernetes, Helm, HPA
- **Observability Layer**: Prometheus, Grafana, Loki
- **Security Layer**: Vault, non-root containers

## Request Flow
1. User sends POST /chat to FastAPI
2. FastAPI checks Redis cache
3. If cache miss, FastAPI calls Ollama
4. Ollama generates response using Mistral
5. Response cached in Redis and returned to user
