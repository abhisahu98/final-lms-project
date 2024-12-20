pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_REPO = "abhishek199/lms-application" // Your DockerHub repository
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Clean Previous Docker Image') {
            steps {
                script {
                    // Delete existing image from DockerHub
                    sh """
                    docker login -u ${DOCKER_CREDENTIALS_USR} -p ${DOCKER_CREDENTIALS_PSW}
                    curl -X DELETE "https://hub.docker.com/v2/repositories/${DOCKERHUB_REPO}/tags/latest/"
                    """
                }
            }
        }

        stage('Build and Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        def image = docker.build("${DOCKERHUB_REPO}:latest")
                        image.push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker pull ${DOCKERHUB_REPO}:latest
                docker stop feedback_system || true && docker rm feedback_system || true
                docker run -d --name feedback_system -p 8000:8000 --env-file .env ${DOCKERHUB_REPO}:latest
                '''
            }
        }
    }
}
