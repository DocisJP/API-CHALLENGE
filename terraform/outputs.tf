output "raw_bucket_name" {
  description = "Name of the raw data S3 bucket"
  value       = local.create_bucket["raw"] ? aws_s3_bucket.data_buckets["raw"].id : data.aws_s3_bucket.existing_buckets["raw"].id
}

output "processed_bucket_name" {
  description = "Name of the processed data S3 bucket"
  value       = local.create_bucket["processed"] ? aws_s3_bucket.data_buckets["processed"].id : data.aws_s3_bucket.existing_buckets["processed"].id
}

output "file_validation_lambda_arn" {
  description = "ARN of the file validation Lambda function"
  value       = aws_lambda_function.file_validation.arn
}

output "data_processing_lambda_arn" {
  description = "ARN of the data processing Lambda function"
  value       = aws_lambda_function.data_processing.arn
}

output "file_validation_lambda_role_arn" {
  description = "ARN of the IAM role for file validation Lambda"
  value       = aws_iam_role.file_validation_lambda_role.arn
}

output "data_processing_lambda_role_arn" {
  description = "ARN of the IAM role for data processing Lambda"
  value       = aws_iam_role.data_processing_lambda_role.arn
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_db_instance.default.endpoint
}

output "alb_hostname" {
  value       = aws_lb.main.dns_name
  description = "Hostname of the Application Load Balancer"
}

output "ecs_cluster_name" {
  value       = aws_ecs_cluster.main.name
  description = "Name of the ECS cluster"
}

output "ecs_service_name" {
  value       = aws_ecs_service.main.name
  description = "Name of the ECS service"
}