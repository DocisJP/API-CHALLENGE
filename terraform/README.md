# Terraform Configuration for Globant Challenge

This directory contains the Terraform configuration for the Globant Challenge project.

## Files

- `main.tf`: Main Terraform configuration file. Contains provider configuration and local variables.
- `variables.tf`: Defines input variables used in the Terraform configuration.
- `outputs.tf`: Specifies the outputs that will be displayed after applying the Terraform configuration.
- `providers.tf`: Configures the AWS provider for Terraform.
- `terraform.tfvars`: Sets values for the defined variables.
- `iam_roles.tf`: Defines IAM roles and policies for ECS tasks, and other services.
- `s3.tf`: Manages S3 bucket resources, notifications, and data sources.
- `sqs.tf`: Manages SQS queues and associated policies to allow S3 bucket notifications.
- `rds.tf`: Configures the RDS instance and related resources.
- `step_functions.tf`: Defines the AWS Step Functions state machine for orchestrating the data processing workflow.
- `networking.tf`: Sets up VPC, subnets, and other networking components.
- `nlb.tf`: Configures the Network Load Balancer and target group.
- `ecs.tf`: Sets up the ECS cluster, task definition, and service.
- `api_gateway.tf`: Configures the API Gateway and VPC Link.
- `ecr.tf`: Sets up the Elastic Container Registry for Docker images.

## Changes in S3 and SQS Setup

- **S3 Bucket Creation**: The `s3.tf` configuration now supports conditional bucket creation based on the `create_bucket` local variable. If `create_bucket` is set to `false`, existing buckets are referenced.
- **S3 Bucket Notifications**: A new S3 bucket notification sends events to an SQS queue (`aws_sqs_queue.etl_queue`) when objects are created in the raw data bucket. The notification depends on the correct configuration of the SQS policy, which allows the S3 bucket to send messages to the queue.
- **SQS Queue Policy**: The `sqs.tf` file now includes an SQS queue policy (`aws_sqs_queue_policy.sqs_policy`) that grants permission to the S3 bucket to send messages to the SQS queue.

## Lambda Functions Removed

- Lambda functions have been removed from the configuration. This affects the steps related to `lambda.tf` and the associated triggers.

## Updated Usage

1. Ensure you have Terraform installed and AWS CLI configured.
2. Navigate to this directory.
3. Initialize Terraform:
   ```
   terraform init
   ```
4. Review the planned changes:
   ```
   terraform plan
   ```
5. Apply the configuration:
   ```
   terraform apply
   ```
6. To destroy the infrastructure when not in use:
   ```
   terraform destroy
   ```

## Notes

- The configuration uses both newly created resources and existing ones, depending on the `create_bucket` local variable in `s3.tf`.
- **S3 Bucket Creation**: If `create_bucket["raw"]` or `create_bucket["processed"]` is `false`, Terraform will reference existing S3 buckets instead of creating new ones.
- **S3 Bucket Notifications**: Notifications are set up on the raw data S3 bucket to trigger events to an SQS queue whenever new objects are created in the bucket.
- The RDS instance is created in a VPC with appropriate security groups.
- A Step Functions state machine orchestrates the data processing workflow.
- ECS tasks run in a Fargate cluster behind a Network Load Balancer.
- API Gateway is set up with a VPC Link to the NLB for private integration.

## Outputs

After applying the configuration, Terraform will output:
- The names of the raw and processed data S3 buckets
- The SQS queue URL
- RDS endpoint information
- NLB DNS name
- ECS cluster and service names
- API Gateway URL

## Step Functions

The Step Functions state machine defined in `step_functions.tf` orchestrates the data processing workflow, including various tasks.

## ECS and Docker

The project uses ECS Fargate to run containerized applications. The Docker image for the application should be built and pushed to the ECR repository created by the `ecr.tf` configuration.

## API Gateway and Network Load Balancer

The API Gateway is set up with a VPC Link to the Network Load Balancer, allowing for private integration with the ECS services running in private subnets.

## Modifying the Infrastructure

To modify the infrastructure, update the corresponding Terraform files. For changes to the containerized application, update the Docker image, push it to ECR, and update the ECS task definition in `ecs.tf` with the new image URL.

