pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('dockerhub-credentials') // Your DockerHub credentials
        DOCKERHUB_REPO = "abhishek199/lms-application" // Your DockerHub repository
        OPENAI_API_KEY = credentials('openai-api-key') // Your OpenAI API Key credential ID in Jenkins
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
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
                if [ ! -f .env ]; then
                    echo "Creating missing .env file..."
                    echo "POSTGRES_DB=feedback_db" >> .env
                    echo "POSTGRES_USER=postgres" >> .env
                    echo "POSTGRES_PASSWORD=12345" >> .env
                    echo "POSTGRES_HOST=db" >> .env
                    echo "POSTGRES_PORT=5432" >> .env
                    echo "REDIS_HOST=redis" >> .env
                    echo "REDIS_PORT=6379" >> .env
                    echo "OPENAI_API_KEY=${OPENAI_API_KEY}" >> .env
                fi
                chmod +x wait-for-it.sh
                dos2unix wait-for-it.sh
                '''
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        def image = docker.build("${DOCKERHUB_REPO}:latest", "--no-cache .")
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
                docker-compose up -d
                docker-compose run --rm web python manage.py makemigrations --no-input
                docker-compose run --rm web python manage.py migrate --no-input
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline execution complete!"
            sh 'docker-compose ps || true'
        }
        failure {
            echo "Pipeline execution failed!"
        }
        success {
            echo "Pipeline executed successfully!"
        }
    }
}
