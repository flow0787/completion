
# Completion
Helps alleviate boredom by talking to the AI of your choosing.

## Features

- Healthchecks for app uptime
- Tracking requests in memory
- Route requests to your AI of choice
 
## Deployment

  - It is meant to run in Kubernetes. Install Minikube per details [here](https://minikube.sigs.k8s.io/docs/start/?arch=/macos/arm64/stable/binary%20download)
  - Add your OpenRouter API key inside `k8s/secret.yml`, base64 encoded
  - Define whatever OpenRouter model you wish to use inside by updating the  `OPENROUTER_MODEL` inside `k8s/deployment.yml`
  - Once Minikube is installed, and all k8s files were updated accordingly run:
```
kubectl apply -f deployment.yml
kubectl apply -f secret.yml
kubectl apply -f service.yml
```  

## Usage

After creating all resources, find the NodePort service endpoint and send requests using cURL:
```
minikube service deployed-service-name --url
curl -X POST $URL:$NODEPORT/completion -H "content-type: application/json" --data '{"prompt": "What is the meaning of life?"}' 
```
To see a history of past requests and their answers (stored in memory - lost on pod restart), run:
`curl -X GET $URL:$NODEPORT/history`

## Constraints and potential improvements
1. Secrets can be handled better by rewriting the deployment files to Helm charts and passing the secret as value at install i.e. `helm upgrade --install adaptai ./mychart \
  --set openrouterApiKey="$OPENROUTER_API_KEY"` or using `csi-secrets-store-driver` to pull the secret from the secrets manager of your choosing (Azure KeyVault, AWS Secrets Manager, etc)