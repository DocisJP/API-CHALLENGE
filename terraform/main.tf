data "aws_s3_bucket" "raw_data" {
  bucket = var.raw_bucket_name
}

data "aws_s3_bucket" "processed_data" {
  bucket = var.processed_bucket_name
}