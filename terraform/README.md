# Terraform Configuration for Globant Challenge

This directory contains the Terraform configuration for the Globant Challenge project.

## Files

- `main.tf`: Main Terraform configuration file. Contains resources for Lambda functions and S3 bucket notifications.
- `variables.tf`: Defines input variables used in the Terraform configuration.
- `outputs.tf`: Specifies the outputs that will be displayed after applying the Terraform configuration.
- `providers.tf`: Configures the AWS provider for Terraform.
- `terraform.tfvars`: Sets values for the defined variables.
- `iam_roles.tf`: Defines IAM roles and policies for Lambda functions.
- `lambda.tf`: Configures Lambda functions and their triggers.
- `s3.tf`: Manages S3 bucket resources and data sources.
- `rds.tf`: Configures the RDS instance and related resources.
- `step_functions.tf`: Defines the AWS Step Functions state machine for orchestrating the data processing workflow.


## Lambda Function Zip Files

- `data_processing_lambda.zip`: Contains the code for the data processing Lambda function.
- `file_validation_lambda.zip`: Contains the code for the file validation Lambda function.

These zip files are created automatically by Terraform using the `archive_file` data source and are used to deploy the Lambda functions.

## Usage

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

- This configuration uses a combination of resources and data sources to manage new resources and reference existing ones.
- S3 buckets can be created or referenced based on the `create_bucket` local variable in `s3.tf`.
- Lambda functions are created and deployed using the source code in the `../lambda_functions` directory.
- The RDS instance is created in a VPC with appropriate security groups.
- A Step Functions state machine orchestrates the data processing workflow.

## Outputs

After applying the configuration, Terraform will output:
- The names of the raw and processed data S3 buckets
- ARNs of the Lambda functions and their IAM roles
- RDS endpoint information
- Step Functions state machine ARN

## Lambda Functions

1. File Validation Lambda:
- Purpose: Validates files uploaded to the raw data S3 bucket.
- Trigger: S3 ObjectCreated events on the raw data bucket.

2. Data Processing Lambda:
- Purpose: Processes validated data from the raw bucket and stores results in the processed bucket.
- Trigger: Invoked as part of the Step Functions workflow.

## Database Setup

The `rds.tf` file includes a `null_resource` that runs Python scripts to set up the database schema and update the configuration. Ensure that the `config.yaml` file is present in the project root directory for these scripts to work correctly.

## Step Functions

The Step Functions state machine defined in `step_functions.tf` orchestrates the data processing workflow, including file validation and data processing steps.

To modify the infrastructure, update the corresponding Terraform files. To change Lambda function code, update the Python files in the `../lambda_functions` directory. Terraform will automatically redeploy the functions on the next `terraform apply`.