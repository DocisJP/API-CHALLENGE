# ecr.tf

resource "aws_ecr_repository" "app_repo" {
  name                 = "globant-data-project-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.data_key.arn
  }

  tags = {
    Name        = "globant-data-project-repo"
    Environment = local.environment
  }
}

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.app_repo.repository_url
}