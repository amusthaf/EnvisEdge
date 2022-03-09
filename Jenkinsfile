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
                sh 'ssh ubuntu@ec2-13-233-73-176.ap-south-1.compute.amazonaws.com rm -f /home/ubuntu/jenkins-test/a'
            }
        }      
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
