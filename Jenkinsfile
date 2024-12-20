pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_REPO = "abhishek199/lms-application"
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
                    sh """
                    docker login -u ${DOCKER_CREDENTIALS_USR} -p ${DOCKER_CREDENTIALS_PSW}
                    curl -X DELETE "https://hub.docker.com/v2/repositories/${DOCKERHUB_REPO}/tags/latest/" || true
                    """
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        def image = docker.build("${DOCKERHUB_REPO}:latest")
                        image.push()
                    }
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    sh '''
                    docker-compose down || true
                    docker-compose pull
                    docker-compose up --build -d
                    '''
                }
            }
        }
    }
}
