pipeline {
    agent any

    environment {
        CI = 'true'
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
                    -Dsonar.sources=backend,frontend ^
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
                    bat 'docker-compose down || exit 0'
                    bat 'docker-compose up -d --build'
                }
            }
        }

        stage('Backend Health Check') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitUntil {
                        bat(script: 'curl http://localhost:5000/health', returnStatus: true) == 0
                    }
                }
            }
        }

        stage('Frontend Ready Check') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitUntil {
                        bat(script: 'curl http://localhost:3000', returnStatus: true) == 0
                    }
                }
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
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs.'
        }
    }
}
