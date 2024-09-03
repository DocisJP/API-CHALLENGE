import os
import boto3
import yaml

# Load configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

config_path = os.path.join(project_root, 'config.yaml')
with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

s3 = boto3.client('s3', region_name=config['aws']['region'])
bucket_name = config['s3']['raw_bucket']

data_folder_path = os.path.join(project_root, 'data')

def upload_file(file_path, file_name):
    print(f"Uploading {file_name} to S3...")
    s3.upload_file(file_path, bucket_name, file_name)
    print(f"File {file_name} uploaded successfully.")

def upload_all_files():
    for filename in os.listdir(data_folder_path):
        if filename.endswith('.csv'):  # Ensure we're only uploading CSV files
            file_path = os.path.join(data_folder_path, filename)
            upload_file(file_path, filename)

if __name__ == "__main__":
    print(f"Starting upload of all CSV files from: {data_folder_path}")
    upload_all_files()
    print("Upload complete.")