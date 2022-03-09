#!/usr/bin/env groovy

pipeline {
   agent any
   stages {
        stage('Build') {
            steps {
                echo 'Build instructions go here...'
            }
        }
        stage('Deploy') {
            steps {
                sh 'ssh ubuntu@ec2-13-233-73-176.ap-south-1.compute.amazonaws.com rm -f /home/ubuntu/jenkins-test/yourfile'
                sh "scp -r $WORKSPACE/EnvisEdge-Python ubuntu@ec2-13-233-73-176.ap-south-1.compute.amazonaws.com:${dest_dir}"
            }
        }      
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
