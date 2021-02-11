#### getPodinfo

##### app
- Python Flask - application is in the directory app, using python k8s client to get the pod details from the cluster.
- Application is exposed using nginx with gunicorn

##### Dockerfile
- build docker image using Dockerfile

##### kind-config
- Using KinD for k8s cluster 
- Kiind config is in the directory kind-config, cluster is provisned using the following commands
```
$ kind create cluster --config kind-cluster-config.yaml --name myk8s
```

##### Helm chart - nginxIngress
- Application is packaged using Helm chart, as Umberlla chart. nginx ingress as Parent chart and respective python application as dependent chart

##### Application1 in namespace1
- update the ingress nodePort as 30080
```
cd nginxIngress
helm dep up . 
helm  install ingress1 . --create-namespace --namespace n1
```
##### Application2 in namespaces2
- update the ingress nodePort as 30081
```
cd nginxIngress
helm dep up . 
helm  install ingress2 . --create-namespace --namespace n2
```

##### Result
- Find the worker node ip
```
$ kubectl get no -o wide
```
- point the localhost to worker node ip in /etc/hosts
- curl localhost:30080 and curl localhost:30081