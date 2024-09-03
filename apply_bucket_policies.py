import yaml
import json
import boto3
import os

# Load config
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Set up S3 client
s3 = boto3.client('s3', region_name=config['aws']['region'])

# Function to read and format policy
def get_formatted_policy(filename):
    with open(os.path.join('aws_jsons', filename), 'r') as file:
        policy = json.load(file)
    
    policy_str = json.dumps(policy)
    formatted_policy = policy_str.replace('${AWS_ACCOUNT_ID}', config['aws']['account_id'])
    formatted_policy = formatted_policy.replace('${S3_RAW_BUCKET}', config['s3']['raw_bucket'])
    formatted_policy = formatted_policy.replace('${S3_PROCESSED_BUCKET}', config['s3']['processed_bucket'])
    
    return formatted_policy

# Apply raw data bucket policy
raw_policy = get_formatted_policy('raw-data-bucket-policy.json')
s3.put_bucket_policy(Bucket=config['s3']['raw_bucket'], Policy=raw_policy)

# Apply processed data bucket policy
processed_policy = get_formatted_policy('processed-data-bucket-policy.json')
s3.put_bucket_policy(Bucket=config['s3']['processed_bucket'], Policy=processed_policy)

print("Bucket policies applied successfully.")