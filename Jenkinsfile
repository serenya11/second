pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building TechMart Docker Image...'
                    sh 'docker build -t flask-techmart .'
                }
            }
        }
        
        stage('Clean Up Old Container') {
            steps {
                script {
                    echo 'Stopping and removing old container if active...'
                    catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                        sh 'docker stop my-techmart-app'
                        sh 'docker rm my-techmart-app'
                    }
                }
            }
        }

        stage('Run New Container') {
            steps {
                script {
                    echo 'Deploying new TechMart store application...'
                    sh 'docker run -d -p 5000:5000 --name my-techmart-app flask-techmart'
                }
            }
        }
    }
}