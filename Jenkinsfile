pipeline {
    agent any

    environment {
        CI = 'true'
        // This 'SonarScanner' name must match what you added in Manage Jenkins -> Tools
        scannerHome = tool 'SonarScanner'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // 'SonarQube' must match the server name in Manage Jenkins -> System
                withSonarQubeEnv('SonarQube') {
                    // Windows batch command using ^ for line breaks
                    bat """
                        "${scannerHome}\\bin\\sonar-scanner" ^
                        -Dsonar.projectKey=elibrary-key ^
                        -Dsonar.sources=. ^
                        -Dsonar.host.url=http://localhost:9000
                    """
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Your fixed path is preserved here
                bat '"C:\\Users\\Krish Chitte\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install selenium' 
            }
        }

        stage('Build & Deploy (Docker)') {
            steps {
                script {
                    try {
                        bat 'docker-compose down'
                    } catch (Exception e) {
                        echo 'No active containers to stop.'
                    }
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
                // Your fixed path is preserved here
                bat '"C:\\Users\\Krish Chitte\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" tests/selenium_test.py'
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