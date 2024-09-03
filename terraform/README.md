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

## Notes

- This configuration uses a combination of resources and data sources to manage new resources and reference existing ones.
- S3 buckets can be created or referenced based on the `create_bucket` local variable in `s3.tf`.
- Lambda functions are created and deployed using the zip files generated from the source code.

## Outputs

After applying the configuration, Terraform will output:
- The names of the raw and processed data S3 buckets
- ARNs of the Lambda functions and their IAM roles

## Lambda Functions

1. File Validation Lambda:
   - Purpose: Validates files uploaded to the raw data S3 bucket.
   - Trigger: S3 ObjectCreated events on the raw data bucket.

2. Data Processing Lambda:
   - Purpose: Processes validated data from the raw bucket and stores results in the processed bucket.
   - Trigger: Invoked as part of the data processing workflow (e.g., by Step Functions, not shown in this config).

To modify the Lambda function code, update the corresponding Python files in the `lambda_functions` directory. Terraform will automatically repackage and redeploy the functions on the next `terraform apply`.