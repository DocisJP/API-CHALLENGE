locals {
  bucket_names = {
    raw       = var.raw_bucket_name
    processed = var.processed_bucket_name
  }
  create_bucket = {
    raw       = false # Set to true if you want to create the bucket
    processed = false # Set to true if you want to create the bucket
  }
}

resource "aws_s3_bucket" "data_buckets" {
  for_each = { for k, v in local.bucket_names : k => v if local.create_bucket[k] }

  bucket = each.value

  force_destroy = false

  tags = {
    Name        = each.value
    Environment = "production"
    Managed_by  = "Terraform"
  }
}

data "aws_s3_bucket" "existing_buckets" {
  for_each = { for k, v in local.bucket_names : k => v if !local.create_bucket[k] }

  bucket = each.value
}