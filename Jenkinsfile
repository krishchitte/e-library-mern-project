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
                        -Dsonar.exclusions=**/node_modules/**,**/build/**,**/dist/**,**/tests/** ^
                        -Dsonar.host.url=http://localhost:9000
                    """
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Install required Python packages using the specific Python executable
                bat '"C:\\Users\\Krish Chitte\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install selenium webdriver-manager' 
            }
        }

        stage('Build & Deploy (Docker)') {
            steps {
                script {
                    try {
                        // Stop any existing containers to ensure a clean slate
                        bat 'docker-compose down'
                    } catch (Exception e) {
                        echo 'No active containers to stop.'
                    }
                    // Build and start the containers in detached mode
                    bat 'docker-compose up -d --build'
                }
            }
        }

        stage('Health Check') {
            steps {
                echo 'Waiting for services to start...'
                // Give containers time to initialize (DB connection, Server listening, etc.)
                sleep 20
            }
        }

        stage('Automated Testing') {
            steps {
                echo 'Running Python Selenium Tests...'
                // Run the Selenium test script using the specific Python executable
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