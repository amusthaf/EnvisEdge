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
                checkout([$class: 'GitSCM', branches: [[name: 'refactor-serializer']], browser: [$class: 'GithubWeb', repoUrl: 'https://github.com/amusthaf/EnvisEdge'], extensions: [[$class: 'CloneOption', honorRefspec: true, noTags: true, reference: '', shallow: false], [$class: 'GitLFSPull'], [$class: 'LocalBranch', localBranch: 'refactor-serializer']], userRemoteConfigs: [[url: 'https://github.com/amusthaf/EnvisEdge']]])
                }
        }      
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
