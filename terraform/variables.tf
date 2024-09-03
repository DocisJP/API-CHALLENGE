variable "aws_region" {
  description = "The AWS region to create resources in"
  type        = string
}

variable "raw_bucket_name" {
  description = "Name of the S3 bucket for raw data"
  type        = string
}

variable "processed_bucket_name" {
  description = "Name of the S3 bucket for processed data"
  type        = string
}
