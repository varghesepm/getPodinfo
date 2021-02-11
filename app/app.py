from flask import Flask, jsonify
from kubernetes import client, config
import os

app = Flask(__name__)

ns_list = [os.environ['NAMESPACE1'], os.environ['NAMESPACE2']]
pod_dict = {}
myPodResult = []

# config.load_kube_config()
# #config.load_incluster_config()
config.load_incluster_config()
v1 = client.CoreV1Api()

@app.route("/")
def mainIndex():
    for ns in ns_list:
        pod_list = v1.list_namespaced_pod(ns, watch=False)
        for pod in pod_list.items:
            if pod.metadata.name.split("-")[0] != "ingress":
                pod_dict[pod.metadata.name] = pod.status.pod_ip
    for k in pod_dict:
        myPodResult.append({
            "POD_IP": pod_dict[k], 
            "POD_NAME": k
        })
    return jsonify(myPodResult)
myPodResult[:] = []

@app.route("/myPodInfo")
def getPodDetails():
    for ns in ns_list:
        pod_list = v1.list_namespaced_pod(ns,watch=False)
        for pod in pod_list.items:
            if pod.metadata.name.split("-")[0] != "nginx":
                pod_dict[pod.metadata.name] = pod.status.pod_ip
    for k in pod_dict:
        myPodResult.append({
            "POD_IP": pod_dict[k], 
            "POD_NAME": k
        })
    return jsonify(myPodResult)
myPodResult[:] = []

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)