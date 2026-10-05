pipeline {
    agent any
    options {
        withBuildUser()
    }
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
                    echo 'Starting the pipeline...'
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
        stage('Trivy Docker Image Scan') {
            steps {
                script {
                    def image = "${DOCKERHUB_REPOSITORY}:${BUILD_NUMBER}"

                    sh """
                docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy:latest \
                    image \
                    --severity CRITICAL \
                    --exit-code 1 \
                    --format table \
                    ${image}
            """
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
    post {
        success {
            emailext(
            subject: "Jenkins Pipeline Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: "The Jenkins pipeline for job '${env.JOB_NAME}' build #${env.BUILD_NUMBER} has completed successfully.\n\nCheck the build details at: ${env.BUILD_URL}",
            to: "${env.BUILD_USER_EMAIL}"
        )
        }
        failure {
            emailext(
            subject: "Jenkins Pipeline Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: "The Jenkins pipeline for job '${env.JOB_NAME}' build #${env.BUILD_NUMBER} has failed.\n\nCheck the build details at: ${env.BUILD_URL}",
            to: "${env.BUILD_USER_EMAIL}"
        )
        }
    }
}
