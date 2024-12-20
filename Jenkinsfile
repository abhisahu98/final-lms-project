pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = credentials('dockerhub-username')
        DOCKERHUB_TOKEN = credentials('dockerhub-token')
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        def image = docker.build("${DOCKERHUB_USERNAME}/feedback_system:latest")
                        image.push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker pull ${DOCKERHUB_USERNAME}/feedback_system:latest
                docker stop feedback_system || true && docker rm feedback_system || true
                docker run -d --name feedback_system -p 8000:8000 --env-file .env ${DOCKERHUB_USERNAME}/feedback_system:latest
                '''
            }
        }
    }
}
