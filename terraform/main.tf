terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  profile    = "terraform"
  region     = "us-east-1"
}

resource "aws_ecr_repository" "lambda_image_repo" {
  name                 = var.ecr_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

data "aws_ecr_image" "lambda_image" {
  depends_on = [
    null_resource.ecr_image
  ]
  repository_name = local.ecr_repository_name
  image_tag       = local.ecr_image_tag
}

resource "aws_iam_role" "lambda_role" {
  name               = "${local.lambda_name}-lambda-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}


data "aws_iam_policy_document" "lambda_policy_doc" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    effect    = "Allow"
    resources = ["*"]
    sid       = "CreateCloudWatchLogs"
  }
}

resource "aws_iam_policy" "lambda_policy" {
  name   = "${local.lambda_name}-lambda-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.lambda_policy_doc.json
}

resource "aws_lambda_function" "lambda_function" {
  depends_on = [
    null_resource.ecr_image
  ]
  function_name = "${local.lambda_name}-lambda"
  role          = aws_iam_role.lambda_role.arn
  timeout       = 30
  image_uri     = "${aws_ecr_repository.lambda_image_repo.repository_url}@${data.aws_ecr_image.lambda_image.id}"
  package_type  = "Image"
  environment {
    variables = {
      DB_USER       = var.db_user
      DB_PASSWORD   = var.db_password
      DB_HOST       = var.host_name
      DB_PORT       = var.db_port
      DB_NAME       = var.db_name
    }
  }
}

resource "aws_lambda_function_url" "lambda_url" {
  function_name      = "${aws_lambda_function.lambda_function.function_name}"
  authorization_type = "NONE"
}

resource "aws_s3_bucket" "my_s3_bucket_fastapi_app"{
  bucket = var.s3_bucket_name
}

resource "aws_s3_object" "terraform_tfstate_object" {
  bucket = var.s3_bucket_name
  key    = "terraform_backup"
  source = "./terraform.tfstate.backup"
}

data "aws_caller_identity" "current_identity" {}

locals {
  account_id          = data.aws_caller_identity.current_identity.account_id
  lambda_name         = var.lambda_name
  ecr_repository_name = var.ecr_name
  region              = "us-east-1"
  ecr_image_tag       = "latest"
}

output "account_id" {
  value = local.account_id
}

output "region" {
  value = local.region
}

resource "null_resource" "ecr_image" {
  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset(path.root, "../src/**") : filesha1(f)]))
  }
  # triggers = {
    # python_file_1 = filemd5("../src/main.py")
    # python_file_2 = filemd5("../plot.py")
    # python_file_3 = filemd5("../tweeter.py")
    # python_file_4 = filemd5("../download.py")
    # requirements  = filemd5("../requirements.txt")
    # docker_file   = filemd5("../Dockerfile")-
  # }
  
  provisioner "local-exec" {
  command = <<EOF
    docker build -t ${var.lambda_name} .. && aws ecr get-login-password --region ${local.region} --profile terraform | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${local.region}.amazonaws.com && docker tag ${local.lambda_name}:${local.ecr_image_tag} ${local.account_id}.dkr.ecr.${local.region}.amazonaws.com/${local.lambda_name}:${local.ecr_image_tag} && docker push ${local.account_id}.dkr.ecr.${local.region}.amazonaws.com/${local.lambda_name}:${local.ecr_image_tag} 
    EOF
  }


}