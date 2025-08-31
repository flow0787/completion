
# Completion
Helps alleviate boredom by talking to the AI of your choosing.

## Features

- Healthchecks for app uptime
- Tracking requests in memory
- Route requests to your AI of choice
 
## Deployment
### Using kuberntes manifests
  - It is meant to run in Kubernetes. Install Minikube per details [here](https://minikube.sigs.k8s.io/docs/start/?arch=/macos/arm64/stable/binary%20download)
  - Add your OpenRouter API key inside `k8s/secret.yml`, base64 encoded
  - Define whatever OpenRouter model you wish to use inside by updating the  `OPENROUTER_MODEL` inside `k8s/deployment.yml`
  - Once Minikube is installed, and all k8s files were updated accordingly run:
```
kubectl apply -f deployment.yml
kubectl apply -f secret.yml
kubectl apply -f service.yml
```  

### Using Helm
Install Helm v3 as per the recommendations [here](https://helm.sh/docs/intro/install/).
```
helm install -f /path/to/adaptai-chart/values.yml $RELEASE_NAME /path/to/adaptai-chart --create-namespace
```

## Usage

After creating all resources, find the NodePort service endpoint and send requests using cURL:
```
minikube service deployed-service-name --url
curl -X POST $URL:$NODEPORT/completion -H "content-type: application/json" --data '{"prompt": "What is the meaning of life?"}' 
```
To see a history of past requests and their answers (stored in memory - lost on pod restart), run:
`curl -X GET $URL:$NODEPORT/history`

## EXTRA

Viewing all data in a unified manner is possible using Grafana stack. It can be installed for Minikube using helm.
```
brew install helm
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install loki grafana/loki-stack --set grafana.enabled=true --set prometheus.enabled=true --set promtail.enabled=true
```

Once installed, find the Grafana admin password and start a service port forward to access it:
```
kubectl get secret loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
kubectl port-forward svc/lok-grafana 3000:80
```

With the application running (remember to start it with `minikube service adaptai-service --url`), start doing requests to either of the available endpoints `/healthcheck`, `/completion`, `/history` to generate data and logs.
View the generated logs inside the browser of your choosing in Grafana -> Explore (Loki datasource) -> Label filters `app == adaptai`

## Constraints and potential improvements
1. Secrets can be handled better by rewriting the deployment files to Helm charts and passing the secret as value at install i.e. `helm upgrade --install adaptai ./mychart \
  --set openrouterApiKey="$OPENROUTER_API_KEY"` or using `csi-secrets-store-driver` to pull the secret from the secrets manager of your choosing (Azure KeyVault, AWS Secrets Manager, etc)
2. `/history` endpoint can be made persistent using either a volume mount and saving to a file or using a light sqlite database or a full-fledged database deployed in kubernetes
3. Prometheus monitoring for all endpoints, for metrics such as requests, latency, etc, can be added by updating the app.py and making use of the prometheus module
4. Log `/history` data so it can be saved in the loki database