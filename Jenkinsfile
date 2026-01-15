pipeline {
    agent any

    environment {
        CI = 'true'
        // Must match Manage Jenkins -> Tools
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
                withSonarQubeEnv('SonarQube') {
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
                bat '"C:\\Users\\Krish Chitte\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install selenium webdriver-manager'
            }
        }

        stage('Build & Deploy (Docker)') {
            steps {
                script {
                    echo 'Stopping old containers (if any)...'
                    bat 'docker-compose down -v || exit 0'

                    echo 'Building and starting containers...'
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
                bat '"C:\\Users\\Krish Chitte\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" tests/selenium_test.py'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker containers and volumes...'
            bat 'docker-compose down -v || exit 0'
            bat 'docker container prune -f || exit 0'
        }

        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}
