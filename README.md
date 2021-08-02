# mlflow-on-kubernetes
Deploying MLflow on Minikube and Openshift 4

Adapted from https://towardsdatascience.com/mlflow-part-2-deploying-a-tracking-server-to-minikube-a2d6671e6455 for Openshift

## Folder structure & pre-requisites

Folder structure:

    .
    ├── Dockerfile
    ├── example
    │   ├── test.txt
    │   ├── train.csv
    │   └── train.py
    ├── k8s
    │   ├── mlflow_deployment.yaml
    │   ├── mlflow_minio.yaml
    │   └── mlflow_postgres.yaml
    └── README.md

Needed images:

- MLflow: As we will need a MLflow docker image in the mlflow_deployment.yaml manifest, look at  https://github.com/pdemeulenaer/mlflow-image to produce such, or simply use the DockerHub image pdemeulenaer/mlflow-server:537

- Postgres: postgres:11

- Minio: minio/minio:RELEASE.2020-07-27T18-37-02Z . Although 1-year old, fits well. For more recent images, need to change logic. 

# How to deploy MLflow on Openshift?

Needed commands:

$ oc login --token=sha256~some_token --server=some-os4-server:port

$ kubectl apply -f mlflow_postgres.yaml

    configmap/mlflow-postgres-config created
    statefulset.apps/mlflow-postgres created
    service/mlflow-postgres-service created

$ kubectl apply -f mlflow_minio.yaml 

    deployment.apps/mlflow-minio created
    service/mlflow-minio-service created
    Warning: networking.k8s.io/v1beta1 Ingress is deprecated in v1.19+, unavailable in v1.22+; use networking.k8s.io/v1 Ingress
    ingress.networking.k8s.io/mlflow-minio-ingress created
    persistentvolumeclaim/mlflow-pvc created

$ oc get pods,services

    NAME                                READY   STATUS              RESTARTS   AGE
    pod/mlflow-minio-64447c6687-bs9rm   0/1     ContainerCreating   0          12s
    pod/mlflow-postgres-0               0/1     ContainerCreating   0          44s

    NAME                              TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
    service/mlflow-minio-service      NodePort   172.30.133.80   <none>        9000:31586/TCP   12s
    service/mlflow-postgres-service   NodePort   172.30.173.63   <none>        5432:30221/TCP   44s

Here I need to change the CLUSTER-IP in the manifest mlflow_deployment.yaml for minio and postgres adresses. Manual step so far...

$ kubectl apply -f mlflow_deployment.yaml 

    deployment.apps/mlflow-deployment created
    service/mlflow-service created
    Warning: networking.k8s.io/v1beta1 Ingress is deprecated in v1.19+, unavailable in v1.22+; use networking.k8s.io/v1 Ingress
    ingress.networking.k8s.io/mlflow-ingress created

Then for openshift we need to create a route: 

$ oc expose service/mlflow-service

    route.route.openshift.io/mlflow-service exposed

Note for Openshift: while using the Openshift free sandbox, I could see that when deploying yaml manifests including images from DockerHub, sometimes I get errors "too many requests", so as if there would be a limit of pulling images. Usually waiting a bit between 2 deployments allowed to clear the issue. But when the issue persists (sometimes it does), a way around would be to import the images within Openshift container registry, for example like this, for the minio image: 

$ oc import-image docker.io/minio/minio –confirm

In the log message following such command is the full address of the image within Openshift container registry.

# How to deploy MLflow on Minikube?

Almost same, just the route creation is not needed within minikube, instead ingress solution working. To enable the addon in minikube:

$ minikube addons list

$ minikube addons enable ingress

Then get the minikube cluster ip address:

$ minikube ip

Then we modify the /etc/hosts file (following https://towardsdatascience.com/mlflow-part-2-deploying-a-tracking-server-to-minikube-a2d6671e6455) so that the browser translates “localhost” to your local IP address. Paste the minikube IP address (which is 192.168.99.104 in my case) followed by BOTH host names for the MLflow server and Minio artifact store (mlflow-server.local and mlflow-minio.local)

    192.168.99.104 mlflow-server.local mlflow-minio.local

