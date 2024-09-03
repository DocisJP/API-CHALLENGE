# AWS JSON Configurations for Globant Challenge

This directory contains JSON configuration files for AWS resources used in the Globant Challenge project.

## Files

- `raw-data-bucket-policy.json`: Policy for the S3 bucket storing raw data.
- `processed-data-bucket-policy.json`: Policy for the S3 bucket storing processed data.

## Usage

These JSON files are used in conjunction with the `apply_bucket_policies.py` script located in the root directory. The script reads these files, replaces placeholders with actual values from the `config.yaml` file, and applies the policies to the respective S3 buckets.

To apply these policies:

1. Ensure the `config.yaml` file in the root directory is properly configured with your AWS account ID and bucket names.
2. Run the `apply_bucket_policies.py` script from the root directory:
   ```
   python apply_bucket_policies.py
   ```

## Policy Details

### Raw Data Bucket Policy

This policy allows:
- PutObject: To upload new raw data files
- GetObject: To retrieve raw data files
- ListBucket: To list the contents of the bucket

### Processed Data Bucket Policy

This policy allows:
- GetObject: To retrieve processed data files
- ListBucket: To list the contents of the bucket

Note: The processed data bucket does not allow PutObject operations directly, as data should only be added through the data processing pipeline.

## Placeholders

Both JSON files use the following placeholders, which are replaced by the Python script:
- `${AWS_ACCOUNT_ID}`: Your AWS account ID
- `${S3_RAW_BUCKET}`: Name of the raw data bucket
- `${S3_PROCESSED_BUCKET}`: Name of the processed data bucket

Ensure these placeholders are not modified in the JSON files, as they are necessary for the Python script to function correctly.