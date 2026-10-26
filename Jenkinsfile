pipeline {
  agent any

  environment {
    // Paste the app_private_ip value from "terraform output"
    APP_IP = '10.0.1.223'
  }

  stages {
    stage('Deploy') {
      steps {
        sshagent(['app-server-key']) {
          sh '''ssh -o StrictHostKeyChecking=no ubuntu@$APP_IP "
            [ -d app ] || git clone https://github.com/praise-oguns/flask-cicd-aws-pipeline.git app
            cd app && git pull && docker compose up -d --build"'''
        }
      }
    }
  }
}
