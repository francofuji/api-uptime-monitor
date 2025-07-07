variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "db_username" {
  description = "Database master username"
  type        = string
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "uptimemonitor"
}

variable "lambda_package" {
  description = "Path to Lambda deployment package zip"
  type        = string
}

variable "jwt_secret" {
  description = "JWT secret for API auth"
  type        = string
  sensitive   = true
}
