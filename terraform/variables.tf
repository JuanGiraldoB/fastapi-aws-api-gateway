variable "ecr_name" {
    description = "Name of the ecr registry"
    type = string
}

variable "s3_bucket_name" {
    description = "Name of the s3 bucket"
    type = string
}

variable "lambda_name" {
    description = "Name of the lambda function"
    type = string
}

# DB variables
variable "host_name" {}
variable "db_user" {}
variable "db_password" {}
variable "db_port" {}
variable "db_name" {}