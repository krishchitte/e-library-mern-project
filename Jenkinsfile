pipeline {
    agent any

    tools {
        // Keeps Node.js for other tasks if needed, though we use Docker mainly now
        nodejs 'NodeJS' 
    }

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
                // Installs Selenium for Python
                // Note: Ensure python3 and pip are installed on your Jenkins machine
                sh 'pip install selenium' 
                // OR on some systems: sh 'pip3 install selenium'
            }
        }

        stage('Build & Deploy (Docker)') {
            steps {
                script {
                    try {
                        sh 'docker-compose down'
                    } catch (Exception e) {
                        echo 'No active containers to stop.'
                    }
                    sh 'docker-compose up -d --build'
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
                // Run the Python script
                sh 'python tests/selenium_test.py'
                // OR on some systems: sh 'python3 tests/selenium_test.py'
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