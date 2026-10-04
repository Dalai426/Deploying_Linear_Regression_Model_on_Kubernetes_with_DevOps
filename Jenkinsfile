pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIAL_ID = ''
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'dalai426/aau'
    }
    stages {
        stage('Start') {
            steps {
                script {
                    echo "Starting the pipeline..."
                    sh 'ls -l'
                }
            }
        }
    }
}