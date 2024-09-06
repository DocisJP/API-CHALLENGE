# main.tf

#Remote state management
terraform {
  backend "s3" {
    bucket  = "globant-data-project-tfstate-12345"
    key     = "terraform.tfstate"
    region  = "sa-east-1"
    encrypt = true
  }
}


locals {
  project_name = "globant-data-project"
  environment  = "production" # or "development", etc.
}


resource "aws_kms_key" "data_key" {
  description             = "KMS key for data encryption"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = {
    Name        = "${local.project_name}-data-key"
    Environment = local.environment
  }
}
