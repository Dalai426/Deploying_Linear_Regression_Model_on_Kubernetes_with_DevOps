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
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }
        stage('Export Docker Image') {
            steps {
                sh """
                    docker save \
                    ${DOCKERHUB_REPOSITORY}:${BUILD_NUMBER} \
                    -o image.tar
                """
            }
        }
        stage('Trivy Docker Image Scan') {
            agent {
                docker {
                    image 'aquasec/trivy:latest'
                    // Mount the Jenkins workspace to the container
                    args '-v ${WORKSPACE}:/workspace'
                }
            }
            steps {
                sh """
                    trivy image \
                    --input /workspace/image.tar \
                    --severity HIGH,CRITICAL \
                    --exit-code 1 \
                    --format table
                """
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