pipeline {
    agent any
    environment {
        // the ID of the DockerHub credentials stored in Jenkins
        DOCKERHUB_CREDENTIAL_ID = 'efb573bb-0222-4486-b7af-429a75f982fe'
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
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:${BUILD_NUMBER}")
                }
            }
        }
stage('Trivy Docker Image Scan') {
    steps {
        script {
            def image = "${DOCKERHUB_REPOSITORY}:${BUILD_NUMBER}"

            sh """
                docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy:latest \
                    image \
                    --severity HIGH,CRITICAL \
                    --exit-code 1 \
                    --format table \
                    ${image}
            """
        }
    }
}
        stage('Lint Code') {
            steps {
                // Lint code
                script {
                        dockerImage.inside() {
                            sh '''
                                python -m pytest ./test/test.py --disable-warnings
                            '''
                        }
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
                        dockerImage.push(env.BUILD_NUMBER)
                    }
                }
            }
        }
    }
}