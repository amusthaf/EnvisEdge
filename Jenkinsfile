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
                sh "scp -r $WORKSPACE/EnvisEdge-Python ubuntu@ec2-13-233-73-176.ap-south-1.compute.amazonaws.com:/home/ubuntu/jenkins-test"
            }
        }      
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
