output "instance_public_ip" {
  description = "Public IP of the Web-Check server"
  value       = aws_instance.web_check.public_ip
}

output "web_check_url" {
  description = "URL to access Web-Check"
  value       = "http://${aws_instance.web_check.public_ip}:3000"
}

output "ssh_command" {
  description = "Command to SSH into the server"
  value       = "ssh -i suresh-key.pem ec2-user@${aws_instance.web_check.public_ip}"
}
