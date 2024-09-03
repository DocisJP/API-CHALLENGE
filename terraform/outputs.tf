output "raw_bucket_name" {
  description = "Name of the raw data S3 bucket"
  value       = data.aws_s3_bucket.raw_data.id
}

output "processed_bucket_name" {
  description = "Name of the processed data S3 bucket"
  value       = data.aws_s3_bucket.processed_data.id
}