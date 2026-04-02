# Incident Handling Runbook

## Scenario 1 - Pod Keeps Crashing
**Detection:** PodRestartingTooMuch alert fires in Grafana
**Diagnose:**
```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous
```
**Resolve:**
```bash
# Check for OOM (Out of Memory)
kubectl describe pod <pod-name> | grep -i oom
# Increase memory limits in values.yaml and upgrade
helm upgrade ai-platform ./helm/ai-platform
```

## Scenario 2 - High Error Rate
**Detection:** HighErrorRate alert fires (>5% errors for 2 minutes)
**Diagnose:**
```bash
kubectl logs deploy/ai-api | grep ERROR
kubectl top pods
```
**Resolve:**
```bash
# Roll back to previous version
kubectl rollout undo deployment/ai-api
# Verify rollback
kubectl rollout status deployment/ai-api
```

## Scenario 3 - High Latency
**Detection:** HighLatency alert fires (p95 > 1 second)
**Diagnose:**
```bash
# Check if HPA has scaled up
kubectl get hpa
# Check Redis connectivity
kubectl exec deploy/ai-api -- env | grep REDIS
```
**Resolve:**
```bash
# Manually scale up if HPA is slow
kubectl scale deployment ai-api --replicas=5
```

## Scenario 4 - Redis Connection Failed
**Detection:** 500 errors on /chat endpoint
**Diagnose:**
```bash
kubectl get pods | grep redis
kubectl logs <redis-pod>
```
**Resolve:**
```bash
# Restart Redis pod
kubectl delete pod <redis-pod>
# App will degrade gracefully until Redis recovers
```

## Scenario 5 - Deployment Rollback
**Detection:** New deployment causing errors
**Diagnose:**
```bash
kubectl rollout history deployment/ai-api
kubectl get pods
```
**Resolve:**
```bash
# Immediate rollback
kubectl rollout undo deployment/ai-api
# Rollback to specific version
kubectl rollout undo deployment/ai-api --to-revision=<N>
# Verify
kubectl rollout status deployment/ai-api
```

## Key Commands Reference
```bash
# Live pod logs
kubectl logs -f deploy/ai-api
# Pod resource usage
kubectl top pods
# Cluster events
kubectl get events --sort-by=.metadata.creationTimestamp
# HPA status
kubectl get hpa
```
