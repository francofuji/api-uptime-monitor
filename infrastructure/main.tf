terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_db_instance" "main" {
  identifier         = "uptime-monitor-db"
  engine             = "postgres"
  instance_class     = "db.t3.micro"
  allocated_storage  = 20
  username           = var.db_username
  password           = var.db_password
  db_name            = var.db_name
  skip_final_snapshot = true
  publicly_accessible = false
}

resource "aws_lambda_function" "api" {
  function_name = "uptime-monitor-api"
  handler       = "app.main.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  filename      = var.lambda_package
  environment {
    variables = {
      DATABASE_URL = aws_db_instance.main.address
      JWT_SECRET   = var.jwt_secret
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "uptime-monitor-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
}

resource "aws_apigatewayv2_api" "http_api" {
  name          = "uptime-monitor-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id             = aws_apigatewayv2_api.http_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.api.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}
