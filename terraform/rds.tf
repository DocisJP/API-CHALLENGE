# rds.tf

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "private_1" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "Private Subnet 1"
  }
}

resource "aws_subnet" "private_2" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "${var.aws_region}b"

  tags = {
    Name = "Private Subnet 2"
  }
}

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
      echo "Current directory: $(pwd)"
      echo "Project root directory contents:"
      ls -la ${path.module}/..
      echo "Scripts directory contents:"
      ls -la ${path.module}/../scripts
      echo "Config file location:"
      ls -la ${path.module}/../config.yaml
      python ${path.module}/../scripts/update_config.py ${aws_db_instance.default.endpoint}
      python ${path.module}/../scripts/setup_db.py
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