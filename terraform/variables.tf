variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

variable "my_ip" {
  description = "Your public IP in CIDR form, for example 203.0.113.10/32"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "public_key_path" {
  description = "Path to your SSH public key"
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}
