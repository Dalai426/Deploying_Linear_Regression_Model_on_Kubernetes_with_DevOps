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
### Prediction
```bash
curl -X POST "http://127.0.0.1:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "MedInc": 5.0,
    "HouseAge": 20.0,
    "AveRooms": 5.5,
    "AveBedrms": 1.0,
    "Population": 1000.0,
    "AveOccup": 3.0,
    "Latitude": 34.0,
    "Longitude": -118.0
  }'
```





