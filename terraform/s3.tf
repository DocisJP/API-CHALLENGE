locals {
  create_bucket = {
    raw       = false,
    processed = false   
  }
}

resource "aws_s3_bucket" "raw_data_bucket" {
  count  = local.create_bucket["raw"] ? 1 : 0
  bucket = var.raw_bucket_name

  tags = {
    Name        = "globant-raw-data-bucket"
    Environment = local.environment
  }
}

resource "aws_s3_bucket" "processed_data_bucket" {
  count  = local.create_bucket["processed"] ? 1 : 0
  bucket = var.processed_bucket_name

  tags = {
    Name        = "globant-processed-data-bucket"
    Environment = local.environment
  }
}

data "aws_s3_bucket" "existing_buckets" {
  for_each = {
    raw       = var.raw_bucket_name
    processed = var.processed_bucket_name
  }

  bucket = each.value
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = local.create_bucket["raw"] ? aws_s3_bucket.raw_data_bucket[0].id : data.aws_s3_bucket.existing_buckets["raw"].id

  queue {
    queue_arn = aws_sqs_queue.etl_queue.arn
    events    = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_sqs_queue_policy.sqs_policy]
}
