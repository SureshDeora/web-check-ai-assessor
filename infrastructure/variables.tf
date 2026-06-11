variable "project_name" {
  description = "Name tag for all resources"
  type        = string
  default     = "web-check"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Name of the AWS key pair for SSH"
  type        = string
  default     = "suresh-key"
}

variable "my_ip" {
  description = "Your IP address for SSH access (CIDR format)"
  type        = string
}

variable "docker_image" {
  description = "Docker image to deploy"
  type        = string
  default     = "lissy93/web-check"
}
