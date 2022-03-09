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
                sh 'ssh rm -f /home/ubuntu/jenkins-test/a'
            }
        }      
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
