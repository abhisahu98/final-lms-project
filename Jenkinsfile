pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('dockerhub-credentials') // Your DockerHub credentials
        DOCKERHUB_REPO = "abhishek199/lms-application" // Your DockerHub repository
        OPENAI_API_KEY = credentials('openai-api-key') // Securely store your OpenAI API key in Jenkins
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir() // Clean the Jenkins workspace
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm // Check out the latest code from the repository
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
                    echo "REDIS_URL=redis://localhost:6379/0" >> .env
                    echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env
                    echo "DJANGO_SETTINGS_MODULE=feedback_system.settings" >> .env
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
                        def image = docker.build("${DOCKERHUB_REPO}:latest", ".")
                        image.push()
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                docker-compose down --remove-orphans
                docker-compose build
                docker-compose up -d

                # Wait for DB and Redis to be ready
                while ! docker-compose exec db pg_isready -U postgres; do
                    echo "Waiting for PostgreSQL to be ready..."
                    sleep 5
                done
                echo "PostgreSQL is ready!"

                while ! docker-compose exec redis redis-cli ping | grep PONG; do
                    echo "Waiting for Redis to be ready..."
                    sleep 5
                done
                echo "Redis is ready!"

                # Apply database migrations
                docker-compose run --rm web python manage.py makemigrations --no-input
                docker-compose run --rm web python manage.py migrate --no-input
                '''
            }
        }

        stage('Test Application') {
            steps {
                sh '''
                curl --fail http://localhost:8000/health || echo "Health check failed!"
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
