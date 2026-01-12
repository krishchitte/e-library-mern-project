pipeline {
    agent any

    environment {
        CI = 'true'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Windows command
                bat 'pip install selenium' 
            }
        }

        stage('Build & Deploy (Docker)') {
            steps {
                script {
                    try {
                        // Windows command
                        bat 'docker-compose down'
                    } catch (Exception e) {
                        echo 'No active containers to stop.'
                    }
                    
                    // Windows command
                    bat 'docker-compose up -d --build'
                }
            }
        }

        stage('Health Check') {
            steps {
                echo 'Waiting for services to start...'
                sleep 20
            }
        }

        stage('Automated Testing') {
            steps {
                echo 'Running Python Selenium Tests...'
                // Windows command
                bat 'python tests/selenium_test.py'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}