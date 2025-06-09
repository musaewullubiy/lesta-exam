pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "lesta-project-web"
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        SSH_CREDENTIALS_ID = "remote-ssh-credentials"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/musaewullubiy/lesta-exam.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -f Dockerfile .'
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: "${SSH_CREDENTIALS_ID}", keyFileVariable: 'SSH_KEY', usernameVariable: 'REMOTE_USER')]) {
                    sh """
                    rsync -avz -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no" \\
                        --exclude='.git' \\
                        --exclude='.env' \\
                        ./ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
                    
                    ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} '
                        cd ${REMOTE_DIR}
                        docker-compose down || true
                        docker-compose up -d --build
                    '
                    """
                }
            }
        }
    }
    post {
        always {
            sh 'docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true'
        }
        failure {
            echo 'Сборка или деплой упали!'
        }
        success {
            echo 'Сборка и деплой прошли успешно!'
        }
    }
}
