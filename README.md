# Globant Data Engineering Challenge

This project implements a scalable, hybrid architecture for processing and analyzing employee hiring data.

## Content
[API](https://github.com/DocisJP/API-CHALLENGE/blob/main/app/README.md)

[AWS_JSONS](https://github.com/DocisJP/API-CHALLENGE/blob/main/aws_jsons/README.md)

[Sripts]([ruta/del/archivo.md](https://github.com/DocisJP/API-CHALLENGE/blob/main/scripts/README.md))

[Terraform]([ruta/del/archivo.md](https://github.com/DocisJP/API-CHALLENGE/blob/main/terraform/README.md))

## Architecture Overview

Our solution combines serverless components for data processing with containerized components for the API. Here's an overview of the architecture:

1. **Data Ingestion**: CSV files are uploaded to an S3 bucket ("globant-raw-data").
2. **Event Notification**: S3 sends an event to SQS when a new file is uploaded.
3. **Data Processing**: An ECS task processes messages from the SQS queue, validates the data, and stores it in Amazon RDS (PostgreSQL).
4. **API**: A containerized FastAPI application, running on AWS ECS, serves the processed data and provides analytical endpoints.
5. **CI/CD**: AWS CodePipeline automates the build and deployment process.

## Architecture Diagram

Key Components:
1. S3 Bucket (Raw Data Storage)
2. SQS Queue (Event Buffer)
3. ECS Cluster
   - ETL Task: Data processing
   - FastAPI Containers: API serving
4. Amazon RDS (PostgreSQL)
5. API Gateway & Application Load Balancer
6. CI/CD Pipeline (CodePipeline, CodeBuild, ECR)

Data Flow:
1. CSV files → S3 Bucket → SQS Queue
2. ECS ETL Task ← SQS Queue
3. ECS ETL Task → RDS
4. User Requests → API Gateway → Load Balancer → FastAPI Containers
5. FastAPI Containers ↔ RDS
6. GitHub → CodePipeline → CodeBuild → ECR → ECS

## API Endpoints

- `POST /upload`: Upload CSV files (handled by S3)
- `GET /metrics/hires`: Get number of employees hired for each job and department in 2021 by quarter
- `GET /metrics/departments`: Get departments that hired more than the mean in 2021

## Setup and Deployment

1. Clone this repository
2. Install AWS CLI and configure your credentials
3. Install Terraform
4. Run `terraform init` and `terraform apply` to provision the infrastructure
5. Build and push the Docker image to ECR
6. Update the ECS task definition with the new image URI
7. Deploy the updated ECS service

## Local Development

Use Docker Compose for local development:

```bash
docker-compose up --build
```
This will start the FastAPI application and a PostgreSQL database locally.

## Testing
Run unit tests:
```bash
 PYTHONPATH=. pytest
```
CI/CD
The CI/CD pipeline is managed by AWS CodePipeline. It's triggered on pushes to the main branch and performs the following steps:

Source: Pull the latest code from CodeCommit
Build: Build the Docker image and run tests
Deploy: Update the ECS service with the new image

Environment Variables
The following environment variables need to be set in the ECS task definition:

AWS_EXECUTION_ENV: Set to "ECS"
SQS_QUEUE_URL: URL of the SQS queue (obtained from Terraform output)
S3_RAW_BUCKET: Name of the S3 bucket for raw data
RDS_ENDPOINT: Endpoint of the RDS instance
RDS_DB_NAME: Name of the database in RDS
RDS_USERNAME: Username for RDS access
RDS_PASSWORD: Password for RDS access

Ensure these variables are properly set in your Terraform configuration and ECS task definition.


