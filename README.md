
## Want to use this project?

### Docker

Build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```



Test it out at:

1. [http://localhost:5080/ping](http://localhost:5080/ping)

In PostMan:
```sh
    http://localhost:5080/api

    JSON:

    {
	    "message":"shajal"
    }
```

### Kubernetes

#### Docker Build

Build and push the images to Docker Hub:

```sh

$ docker build -t shajalahamedcse/service_1 ./service_1
$ docker push shajalahamedcse/service_1

$ docker build -t shajalahamedcse/service_2 ./service_2
$ docker push shajalahamedcse/service_2


```

> Make sure to replace `shajalahamedcse` with your Docker Hub namespace.

#### Kubernetes Deployment

I used metallb for loadbalancing as it an onpremise kubernetes cluster. My local dev was not working that why i deployed it using `kubeadm`.

Create the deployment:

```sh
$ kubectl create -f ./kubernetes/ipay_service_one_deployment.yml
$ kubectl create -f ./kubernetes/ipay_service_two_deployment.yml
```

Create the service:

```sh
$ kubectl create -f ./kubernetes/ipay_service_one_service.yml
$ kubectl create -f ./kubernetes/ipay_service_two_service.yml

```


Try it out in PostMan:

```sh

    http://118.67.213.77:5000/api

    JSON:

        {
	        "message":"shajal"
        }
```


#### AWS :

If I use AWS to deploy it . Then I will use AWS EKS for kubernetes.


#### CI/CD Using Jenkins

There are two way to use Jenkins to deploy in kubernetes. Install Jenkins on a different server or deploy it into the kubernetes cluster in different namespace. I have installed it into diffrent server and installed `kubelet` . Then copied the `kube-config` on the jenkins server. Then used this pipeline to do the build and deploy automation.

```sh

pipeline {
    // Define All variables
  environment {
    BUILD_NUMBER = "0.0.1"
    DOCKER_USERNAME = "use_your_username"
    DOCKER_PASSWORD = "use_your_pass"
    service1_name = 'service_1'
	service2_name = 'service_2'
    
	service1_image_tag = "${DOCKER_USERNAME}/${service1_name}:v${BUILD_NUMBER}"
	service2_image_tag = "${DOCKER_USERNAME}/${service2_name}:v${BUILD_NUMBER}"
  }

  agent any

  stages {
    stage('Build') {
      steps {
        checkout scm
        sh '''
          docker build -t $service1_image_tag ./service_1
          docker build -t $service2_image_tag ./service_2
        '''
      }
    }

    stage('Image Release') {

      steps {

          sh '''
            docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
            docker push $service1_image_tag
            docker push service2_image_tag
          '''

      }
    }
    stage('Deployment') {

      steps {
        sh '''
          kubectl apply -f ./kubernetes/ipay_service_one_deployment.yml
          kubectl apply -f ./kubernetes/ipay_service_two_deployment.yml
        '''
      }
    }
    }
}
```