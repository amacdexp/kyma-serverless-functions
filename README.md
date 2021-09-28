# kyma-serverless-functions
Kyma Serverless function examples  

Includes a: 
> 1. Basic Hello World
> 2. Basic Hello Hana (needs Hana DB, e.g. [Hana Cloud trial](https://www.sap.com/cmp/td/sap-hana-cloud-trial.html) 


[K8S Kyma Serverless functions linked to git repositories](https://kyma-project.io/docs/components/serverless#tutorials-create-a-function-from-git-repository-sources)


# Create git repository secret  
```
kubectl apply -n <namespace> --kubeconfig ~/.kube/kubeconfig.yaml -f - <<EOF
 apiVersion: v1
 kind: Secret
 metadata:
   name: git-creds-key
   namespace: <namespace>
 type: Opaque
 data:
   key: [insert private ssh key (BASE64 encoded) here, e.g. under .ssl]
EOF
```
  
# Create link to GIT Repository  
```
kubectl apply -n <namespace> --kubeconfig ~/.kube/kubeconfig.yaml -f - <<EOF
apiVersion: serverless.kyma-project.io/v1alpha1
kind: GitRepository
metadata:
  name: kyma-serverless-functions
  namespace: <namespace>
spec:
  url: "git@github.com:amacdexp/kyma-serverless-functions.git"
  auth:
    type: "key"
    secretName: "git-creds-key"
EOF
``` 

  
# Python 3.8 Hello World 
```
kubectl apply -n <namespace> --kubeconfig ~/.kube/kubeconfig.yaml -f - <<EOF  
apiVersion: serverless.kyma-project.io/v1alpha1
kind: Function
metadata:
  name: py-hello-world
  namespace: <namespace>
spec:
  type: git
  runtime: python38
  source: kyma-serverless-functions
  reference: main
  baseDir: py-hello-world
EOF
``` 

# Create HANA endpoint configmap
```
kubectl apply -n <namespace>  -f - <<EOF  
apiVersion: v1
kind: ConfigMap
metadata:
  name: hana-endpoint
  namespace: <namespace>
data:
  host: "<endpoint hostname of Hana.. no https>"
  port: "<port>"
EOF
```

# Create HANA db secret  
```
kubectl apply -n <namespace> -f - <<EOF
 apiVersion: v1
 kind: Secret
 metadata:
   name: hana-creds-key
   namespace: i337529
 type: kubernetes.io/basic-auth
 data:
  username: <BASE64 User id>
  password: <Base64 Password>
EOF
``` 



# Python 3.8 Hello Hana
```
kubectl apply -n <namespace> --kubeconfig ~/.kube/kubeconfig.yaml -f - <<EOF  
apiVersion: serverless.kyma-project.io/v1alpha1
kind: Function
metadata:
  name: py-hello-hana
  namespace: <namespace>
spec:
  type: git
  runtime: python38
  source: kyma-serverless-functions
  reference: main
  baseDir: py-hello-hana
  env:
    - name: HANA_HOST
      valueFrom:
        configMapKeyRef:
          name: hana-endpoint
          key: host
    - name: HANA_PORT
      valueFrom:
        configMapKeyRef:
          name: hana-endpoint
          key: port
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: hana-creds-key
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: hana-creds-key
          key: password
EOF
``` 


# Troubleshooting
[Kubectl cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
```
kubectl cluster-info -n <namespace>
kubectl get functions -n <namespace>
kubectl api-resources
kubectl get gitrepositories -n <namespace>
kubectl get pods -n <namespace>
kubectl get pods -o=name --field-selector=status.phase=Running -n <namespace> | grep py-hello-world
kubectl get pods -l 'serverless.kyma-project.io/function-name in (py-hello-world)' --field-selector=status.phase=Running   -n i337529 --output=jsonpath={.items..metadata.name}

kubectl exec -n i337529 --stdin --tty $(kubectl get pods -l 'serverless.kyma-project.io/function-name in (py-hello-world)' --field-selector=status.phase=Running   -n i337529 --output=jsonpath={.items..metadata.name}) -- cat kubeless.py

kubectl exec -n i337529 --stdin --tty $(kubectl get pods -l 'serverless.kyma-project.io/function-name in (py-hello-world)' --field-selector=status.phase=Running   -n i337529 --output=jsonpath={.items..metadata.name}) -- /bin/sh


```
