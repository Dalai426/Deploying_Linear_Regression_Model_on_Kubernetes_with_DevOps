**Container Registry**
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=https://registry.hub.docker.com \
  --docker-username=dalai426 \
  --docker-password=''

**Prepare Kubernetes For Jenkins**
kubectl create sa jenkins
kubectl create clusterrolebinding jenkins --clusterrole=cluster-admin --serviceaccount=default:jenkins
kubectl create token jenkins
