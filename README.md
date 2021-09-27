# kyma-serverless-functions
Kyma Serverless function examples

[K8S Kyma Serverless functions linked to git repositories] (https://kyma-project.io/docs/components/serverless#tutorials-create-a-function-from-git-repository-sources)


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
  
  
# Troubleshooting
```
kubectl cluster-info
kubectl get functions -n <namespace>
```
