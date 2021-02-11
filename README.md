#### getPodinfo

##### app
- Python Flask - application is in the directory app, using python k8s client to get the pod details from the cluster.
- Application is exposed using nginx with gunicorn

##### Dockerfile
- build docker image using Dockerfile
```
$ docker build -t podinfoapp:tag-01 .
```
- images can be found in https://hub.docker.com/r/mmebin/podinfoapp1

##### kind-config
- Using KinD for k8s cluster 
- Kiind config is in the parent directory, cluster is provisned using the following commands
```
$ kind create cluster --config kind-cluster-config.yaml --name myk8s
```

##### Helm chart - nginxIngress
- Application is packaged using Helm chart, as Umberlla chart. nginx ingress as Parent chart and respective python application (podApp) as dependent chart
- official nginx ingress helm chart is used in this repo
```
dependencies:
- name: podApp
  version: "1.2.0"
  repository: file://../podApp
```

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
- curl localhost:30080 and curl localhost:30081 to get the result

##### Metric server and hpa
- Metric server is deployed using normal manifest file 
- both application will scale based on cpu/memory