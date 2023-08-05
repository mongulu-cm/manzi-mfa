# Manzi-mfa

# Prerequesites
Share the pipedream webhook


# Installation
```sh
kubectl create namespace easyappointments

helm repo add jetstack https://charts.jetstack.io
helm update
helm upgrade cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true
kubectl apply -f manifests/issuer-acme.yml

helm install easyappointments . -n easyappointments
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace
kubectl apply -f manifests/parameter-store.yml
```

## Ressources
https://github.com/highcanfly-club/easyappointments-k8s
https://external-secrets.io/latest/introduction/getting-started/
https://external-secrets.io/latest/provider/aws-parameter-store/
https://www.youtube.com/watch?v=DvXkD0f-lhY