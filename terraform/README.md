
# Terraform Configuration for Globant Challenge

This directory contains the Terraform configuration for the Globant Challenge project.

## Files

- `main.tf`: Main Terraform configuration file. Contains data sources for existing S3 buckets.
- `variables.tf`: Defines input variables used in the Terraform configuration.
- `outputs.tf`: Specifies the outputs that will be displayed after applying the Terraform configuration.
- `providers.tf`: Configures the AWS provider for Terraform.
- `terraform.tfvars`: Sets values for the defined variables.

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

- This configuration uses data sources to reference existing S3 buckets, rather than managing their lifecycle.
- The S3 buckets were created manually and are referenced here for documentation and potential future management.

## Outputs

After applying the configuration, Terraform will output:
- The name of the raw data S3 bucket
- The name of the processed data S3 bucket






