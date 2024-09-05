# rds.tf

resource "aws_db_subnet_group" "default" {
  name       = "main"
  subnet_ids = [aws_subnet.private_1.id, aws_subnet.private_2.id]

  tags = {
    Name = "My DB subnet group"
  }
}

resource "aws_security_group" "rds" {
  name        = "rds_sg"
  description = "Allow inbound traffic for RDS"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow inbound from VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds_sg"
  }
}

resource "aws_db_instance" "default" {
  identifier           = "globantdb"
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "16.4"
  instance_class       = "db.t3.micro"
  db_name              = "globantdb"
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.postgres16"
  skip_final_snapshot  = true

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.default.name

  tags = {
    Name = "GlobantRDS"
  }
}

resource "null_resource" "db_setup" {
  depends_on = [aws_db_instance.default]

  provisioner "local-exec" {
    command = <<EOT
      pwd
      ls -la ../scripts
      python ../scripts/update_config.py ${aws_db_instance.default.endpoint}
      python ../scripts/setup_db.py
    EOT

    environment = {
      DB_ENDPOINT = aws_db_instance.default.endpoint
      DB_NAME     = aws_db_instance.default.db_name
      DB_USERNAME = var.db_username
      DB_PASSWORD = var.db_password
      DB_PORT     = aws_db_instance.default.port
    }
  }
}