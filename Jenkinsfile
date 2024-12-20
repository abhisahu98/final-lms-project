pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('dockerhub-credentials')
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
                        def image = docker.build("feedback_system:latest")
                        image.push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker pull feedback_system:latest
                docker stop feedback_system || true && docker rm feedback_system || true
                docker run -d --name feedback_system -p 8000:8000 --env-file .env feedback_system:latest
                '''
            }
        }
    }
}
