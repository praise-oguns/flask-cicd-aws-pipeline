#!/bin/bash
set -e
apt-get update -y
apt-get install -y docker.io git
systemctl enable --now docker
docker run -d --name jenkins --restart unless-stopped \
  -p 8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts-jdk17
