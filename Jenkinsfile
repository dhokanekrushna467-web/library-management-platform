pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        DOCKER_IMAGE_NAME = 'library-management-platform'
        IMAGE_TAG = "v1.${BUILD_NUMBER}"
    }

    stages {

        stage('SCM Checkout') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Environment Setup & Dependencies') {
            steps {
                echo 'Setting up Python environment...'
                bat '''
                    py -3.11 -m venv venv
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Code Linting & Syntax Gate') {
            steps {
                echo 'Running Flake8 checks...'
                bat '''
                    venv\\Scripts\\flake8.exe app database --count --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }

        stage('Automated Unit & Integration Tests') {
            steps {
                echo 'Running Pytest test suite...'
                bat '''
                    if not exist reports mkdir reports
                    venv\\Scripts\\pytest.exe -v --cov=app --junitxml=reports\\test-results.xml tests
                '''
            }
        }

        stage('Build Docker Artifact') {
            steps {
                echo "Building Docker image ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}..."
                bat '''
                    docker build -t %DOCKER_IMAGE_NAME%:%IMAGE_TAG% .
                    docker tag %DOCKER_IMAGE_NAME%:%IMAGE_TAG% %DOCKER_IMAGE_NAME%:latest
                '''
            }
        }

        stage('Kubernetes Minikube Deployment') {
            steps {
                echo 'Deploying application to Minikube...'
                bat '''
                    minikube image load %DOCKER_IMAGE_NAME%:%IMAGE_TAG%
                    kubectl apply -f k8s\\deployment.yaml
                    kubectl apply -f k8s\\service.yaml
                    kubectl set image deployment/library-deployment library-app=%DOCKER_IMAGE_NAME%:%IMAGE_TAG%
                    kubectl rollout status deployment/library-deployment --timeout=120s
                '''
            }
        }
    }

    post {
        always {
            echo 'Archiving test reports...'
            junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
            cleanWs deleteDirs: true, notFailBuild: true
        }

        success {
            echo "CI/CD Pipeline completed successfully for build #${BUILD_NUMBER}!"
        }

        failure {
            echo "Build #${BUILD_NUMBER} FAILED! Check the console output."
        }
    }
}