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
                sh "rm -rf ubuntu@ec2-65-1-51-157.ap-south-1.compute.amazonaws.com:/home/ubuntu/jenkins-test/EnvisEdge-Python/.git"
                sh "scp -r /var/lib/jenkins/workspace/EnvisEdge-Python ubuntu@ec2-65-1-51-157.ap-south-1.compute.amazonaws.com:/home/ubuntu/jenkins-test"
            }
        }      
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
