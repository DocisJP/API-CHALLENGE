# outputs.tf

output "raw_bucket_name" {
  value = local.create_bucket["raw"] ? aws_s3_bucket.raw_data_bucket[0].id : data.aws_s3_bucket.existing_buckets["raw"].id
}

output "processed_bucket_name" {
  value = local.create_bucket["processed"] ? aws_s3_bucket.processed_data_bucket[0].id : data.aws_s3_bucket.existing_buckets["processed"].id
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

output "sqs_queue_url" {
  value = aws_sqs_queue.etl_queue.url
}