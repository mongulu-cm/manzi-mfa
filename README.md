# Manzi mfa
> [Fe'fe'](https://fr.wikipedia.org/wiki/Nufi) language meaning bridge for work in French

## Prerequisites
* Have a minimum of competence on k8s and admin access to one cluster
* Have a [pipedream](https://pipedream.com/) account and fork [workflow ](https://pipedream.com/new?h=tch_wGKfvD)

aaaa

## Deployment
```sh
helm repo add jetstack https://charts.jetstack.io
helm update
helm upgrade cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true
kubectl apply -f manifests/issuer-acme.yml

kubectl create namespace easyappointments
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
