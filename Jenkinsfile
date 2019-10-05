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
    stage('Staging Deployment') {

      steps {
        sh '''
          kubectl create -f ./kubernetes/ipay_service_one_deployment.yml
          kubectl create -f ./kubernetes/ipay_service_two_deployment.yml
        '''
      }
    }
    }
}