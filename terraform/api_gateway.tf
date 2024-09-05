# api_gateway.tf

resource "aws_api_gateway_rest_api" "main" {
  name        = "globant-data-project-api"
  description = "API Gateway for Globant Data Project"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name        = "globant-data-project-api"
    Environment = local.environment
  }
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.proxy.http_method

  integration_http_method = "ANY"
  type                    = "HTTP_PROXY"
  uri                     = "http://${aws_lb.main.dns_name}/{proxy}"

  connection_type = "VPC_LINK"
  connection_id   = aws_api_gateway_vpc_link.main.id

  depends_on = [aws_lb.main]
}

resource "aws_api_gateway_vpc_link" "main" {
  name        = "globant-data-project-vpc-link"
  description = "VPC Link for Globant Data Project"
  target_arns = [aws_lb.main.arn]

  depends_on = [aws_lb.main]
}

resource "aws_api_gateway_deployment" "main" {
  depends_on = [aws_api_gateway_integration.proxy]

  rest_api_id = aws_api_gateway_rest_api.main.id
  stage_name  = "prod"

  lifecycle {
    create_before_destroy = true
  }
}

output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = aws_api_gateway_deployment.main.invoke_url
}