pipeline {
    agent any
    environment {
        // the ID of the DockerHub credentials stored in Jenkins
        DOCKERHUB_CREDENTIAL_ID = 'efb573bb-0222-4486-b7af-429a75f982fe'
        DOCKERHUB_REGISTRY = 'https://index.docker.io/v1/'
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
        stage('Kubernetes Secret') {
            steps {
                withKubeConfig(caCertificate: '', clusterName: 'minikube', contextName: 'minikube', credentialsId: 'kubernete', namespace: 'default', restrictKubeConfigAccess: false, serverUrl: 'https://host.docker.internal:56372') {
                    withCredentials([
                        usernamePassword(
                            credentialsId: "${DOCKERHUB_CREDENTIAL_ID}",
                            usernameVariable: 'DOCKERHUB_USERNAME',
                            passwordVariable: 'DOCKERHUB_TOKEN'
                        )
                    ]) {
                        sh '''
                    kubectl delete secret dockerhub-secret --ignore-not-found
                    kubectl create secret docker-registry dockerhub-secret \
                    --docker-server="${DOCKERHUB_REGISTRY}" \
                    --docker-username="${DOCKERHUB_USERNAME}" \
                    --docker-password="${DOCKERHUB_TOKEN}"
                    '''
                    }
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
        stage('Kubernetes Deployment') {
            steps {
                withKubeConfig(caCertificate: '', clusterName: 'minikube', contextName: 'minikube', credentialsId: 'kubernete', namespace: 'default', restrictKubeConfigAccess: false, serverUrl: 'https://host.docker.internal:56372') {
                    sh '''
                        echo "=== Kubernetes Context ==="
                        kubectl config current-context
                        kubectl cluster-info
                        ls ./kubernetes
                        IMAGE="$DOCKERHUB_REPOSITORY:$BUILD_NUMBER"
                        sed "s|DOCKER_IMAGE|$IMAGE|g" ./kubernetes/kube-deployment.yml | kubectl apply -f -
                        kubectl apply -f ./kubernetes/kube-service.yml
                    '''
                }
            }
        }
    }
}
