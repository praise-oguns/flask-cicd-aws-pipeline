output "jenkins_url" {
  value = "http://${aws_instance.jenkins.public_ip}:8080"
}

output "jenkins_public_ip" {
  value = aws_instance.jenkins.public_ip
}

output "app_url" {
  value = "http://${aws_instance.app.public_ip}"
}

output "app_public_ip" {
  value = aws_instance.app.public_ip
}

output "app_private_ip" {
  value = aws_instance.app.private_ip
}
