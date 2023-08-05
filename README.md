# Manzi-mfa

# Prerequesites
Share the pipedream webhook


# Installation
```sh
kubectl create namespace easyappointments
helm install easyappointments . -n easyappointments
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace
kubectl apply -f external-secrets
```

## Ressources
https://github.com/highcanfly-club/easyappointments-k8s
https://external-secrets.io/latest/introduction/getting-started/
https://external-secrets.io/latest/provider/aws-parameter-store/