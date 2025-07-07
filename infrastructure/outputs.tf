output "api_url" {
  value = aws_apigatewayv2_stage.default.invoke_url
}

output "db_endpoint" {
  value = aws_db_instance.main.endpoint
}
