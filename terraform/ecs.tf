# ecs.tf

resource "aws_ecs_cluster" "main" {
  name = "globant-data-project-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name        = "globant-data-project-cluster"
    Environment = local.environment
  }

}

resource "aws_ecs_task_definition" "app" {
  family                   = "globant-data-project-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "app"
      image = "${aws_ecr_repository.app_repo.repository_url}:latest"
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
      environment = [
        {
          name  = "AWS_EXECUTION_ENV"
          value = "ECS"
        },
        {
          name  = "SQS_QUEUE_URL"
          value = aws_sqs_queue.etl_queue.url
        },
        {
          name  = "S3_RAW_BUCKET"
          value = local.create_bucket["raw"] ? aws_s3_bucket.raw_data_bucket[0].id : data.aws_s3_bucket.existing_buckets["raw"].id
        },
        {
          name  = "S3_PROCESSED_BUCKET"
          value = local.create_bucket["processed"] ? aws_s3_bucket.processed_data_bucket[0].id : data.aws_s3_bucket.existing_buckets["processed"].id
        },
        {
          name  = "RDS_ENDPOINT"
          value = aws_db_instance.default.endpoint
        },
        {
          name  = "RDS_DB_NAME"
          value = aws_db_instance.default.db_name
        },
        {
          name  = "RDS_USERNAME"
          value = aws_db_instance.default.username
        },
        {
          name  = "RDS_PASSWORD"
          value = aws_db_instance.default.password
        }
      ]
    }
  ])
}


resource "aws_ecs_service" "main" {
  name            = "globant-data-project-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.app_count
  launch_type     = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.ecs_tasks.id]
    subnets         = [aws_subnet.private_1.id, aws_subnet.private_2.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app_new.arn
    container_name   = "app"
    container_port   = var.app_port
  }

  depends_on = [aws_lb_listener.front_end]

  tags = {
    Name        = "globant-data-project-service"
    Environment = local.environment
  }
}

resource "aws_security_group" "ecs_tasks" {
  name        = "ecs-tasks-sg"
  description = "Allow inbound access from the NLB only"
  vpc_id      = aws_vpc.main.id

  ingress {
    protocol    = "tcp"
    from_port   = var.app_port
    to_port     = var.app_port
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "ecs-tasks-sg"
    Environment = local.environment
  }
}