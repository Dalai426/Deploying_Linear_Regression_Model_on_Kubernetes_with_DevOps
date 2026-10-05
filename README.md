### Container Registry**
```bash
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=https://registry.hub.docker.com \
  --docker-username=dalai426 \
  --docker-password=''
```

### Prepare Kubernetes For Jenkins
```bash
kubectl create sa jenkins
kubectl create clusterrolebinding jenkins --clusterrole=cluster-admin --serviceaccount=default:jenkins
```

```yml
apiVersion: v1
kind: Secret
metadata:
  name: jenkins-token
  namespace: default
  annotations:
    kubernetes.io/service-account.name: jenkins
type: kubernetes.io/service-account-token
kubectl apply -f jenkins-token.yaml
```





