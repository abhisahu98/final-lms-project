pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_REPO = "abhishek199/lms-application"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir() // Clean the Jenkins workspace
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Docker Environment') {
            steps {
                sh '''
                chmod +x wait-for-it.sh
                dos2unix wait-for-it.sh
                '''
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

        stage('Deploy Application') {
            steps {
                sh '''
                docker-compose down --volumes
                docker-compose build --no-cache
                docker-compose up --build -d
                docker-compose run --rm web python manage.py makemigrations --no-input
                docker-compose run --rm web python manage.py migrate --no-input
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline execution complete!"
            sh 'docker-compose ps'
        }
        failure {
            echo "Pipeline execution failed!"
        }
        success {
            echo "Pipeline executed successfully!"
        }
    }
}
