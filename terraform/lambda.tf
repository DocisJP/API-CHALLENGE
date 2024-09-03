# File Validation Lambda
data "archive_file" "file_validation_lambda" {
  type        = "zip"
  source_file = "${path.module}/../lambda_functions/file_validation/file_validation_lambda.py"
  output_path = "${path.module}/file_validation_lambda.zip"
}

resource "aws_lambda_function" "file_validation" {
  filename         = data.archive_file.file_validation_lambda.output_path
  function_name    = "file_validation"
  role             = aws_iam_role.file_validation_lambda_role.arn
  handler          = "file_validation_lambda.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = data.archive_file.file_validation_lambda.output_base64sha256
}

# Data Processing Lambda
data "archive_file" "data_processing_lambda" {
  type        = "zip"
  source_file = "${path.module}/../lambda_functions/data_processing/data_processing_lambda.py"
  output_path = "${path.module}/data_processing_lambda.zip"
}

resource "aws_lambda_function" "data_processing" {
  filename         = data.archive_file.data_processing_lambda.output_path
  function_name    = "data_processing"
  role             = aws_iam_role.data_processing_lambda_role.arn
  handler          = "data_processing_lambda.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = data.archive_file.data_processing_lambda.output_base64sha256
}

# S3 trigger for file validation Lambda
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = local.create_bucket["raw"] ? aws_s3_bucket.data_buckets["raw"].id : data.aws_s3_bucket.existing_buckets["raw"].id

  lambda_function {
    lambda_function_arn = aws_lambda_function.file_validation.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_validation.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = local.create_bucket["raw"] ? aws_s3_bucket.data_buckets["raw"].arn : data.aws_s3_bucket.existing_buckets["raw"].arn
}