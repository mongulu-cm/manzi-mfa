# Manzi mfa
> [Fe'fe'](https://fr.wikipedia.org/wiki/Nufi) language meaning bridge for work in French

## Prerequisites
* Have a minimum of competence on k8s and admin access to one cluster
* Have a [pipedream](https://pipedream.com/) account and fork [workflow ](https://pipedream.com/new?h=tch_wGKfvD)


## Deployment

Firstly, install all required tools:
```sh
helm repo add jetstack https://charts.jetstack.io
helm repo add external-secrets https://charts.external-secrets.io
helm update
helm upgrade cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true
kubectl apply -f manifests/issuer-acme.yml
helm upgrade external-secrets external-secrets/external-secrets -n external-secrets --create-namespace
kubectl apply -f manifests/parameter-store.yml
kubectl apply -f manifests/diun.yml

NAMESPACE="arc-systems"
helm install arc \
    --namespace "${NAMESPACE}" \
    --create-namespace \
    oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
NAMESPACE="arc-runners"
INSTALLATION_NAME="arc-runner-set"
GITHUB_CONFIG_URL="https://github.com/mongulu-cm/manzi-mfa"
helm upgrade "${INSTALLATION_NAME}" \
    --namespace "${NAMESPACE}" \
    --set githubConfigUrl="${GITHUB_CONFIG_URL}" \
    --set githubConfigSecret=github-arc-secret \
    --set containerMode.type=dind \
    oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
kubectl create secret generic github-arc-secret --namespace=arc-runners --from-literal=github_token=<TOKEN>
```

then start the application:
```sh
kubectl create namespace easyappointments
helm upgrade easyappointments ./helm -n easyappointments
```

## Ressources
https://github.com/highcanfly-club/easyappointments-k8s  
https://external-secrets.io/latest/introduction/getting-started/  
https://external-secrets.io/latest/provider/aws-parameter-store/  
https://www.youtube.com/watch?v=DvXkD0f-lhY  
