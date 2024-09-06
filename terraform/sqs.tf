resource "aws_sqs_queue" "etl_queue" {
  name                      = "globant-etl-queue"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10

  tags = {
    Environment = "production"
  }
}

resource "aws_sqs_queue_policy" "sqs_policy" {
  queue_url = aws_sqs_queue.etl_queue.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.etl_queue.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = local.create_bucket["raw"] ? aws_s3_bucket.raw_data_bucket[0].arn : data.aws_s3_bucket.existing_buckets["raw"].arn
          }
        }
      }
    ]
  })
}
