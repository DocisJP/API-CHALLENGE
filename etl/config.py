import yaml
import os
from pathlib import Path
import datetime

NULL_DATE_PLACEHOLDER = datetime.datetime(1900, 1, 1)

def detect_environment():
    if 'AWS_EXECUTION_ENV' in os.environ:
        return 'aws'
    elif 'DOCKER_CONTAINER' in os.environ or os.path.exists('/.env'):
        return 'docker'
    else:
        return 'local'

def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    
    environment = detect_environment()
    print(f"Detected environment: {environment}")

    if environment == 'aws':
        config['db'] = config['rds']
        config['paths']['data_dir'] = '/tmp/data'
        config['aws'] = {
            'sqs_queue_url': os.environ.get('SQS_QUEUE_URL'),
            's3_raw_bucket': os.environ.get('S3_RAW_BUCKET'),
            's3_processed_bucket': os.environ.get('S3_PROCESSED_BUCKET')
        }
    elif environment == 'docker':
        config['db'] = {
            'host': 'db', 
            'port': 5432,
            'db_name': config['local_db']['db_name'],
            'username': config['local_db']['username'],
            'password': config['local_db']['password']
        }
        config['paths']['data_dir'] = '/app/data'
    else:
        config['db'] = config['local_db']

    return config

CONFIG = load_config()

DB_PARAMS = {
    'dbname': CONFIG['db']['db_name'],
    'user': CONFIG['db']['username'],
    'password': CONFIG['db']['password'],
    'host': CONFIG['db']['host'],
    'port': CONFIG['db']['port']
}

DATA_DIR = Path(CONFIG['paths']['data_dir'])

print(f"Using database host: {DB_PARAMS['host']}")
print(f"Using database port: {DB_PARAMS['port']}")
print(f"Using data directory: {DATA_DIR}")

if detect_environment() == 'aws':
    print(f"Using SQS Queue URL: {CONFIG['aws']['sqs_queue_url']}")
    print(f"Using S3 Raw Bucket: {CONFIG['aws']['s3_raw_bucket']}")
    print(f"Using S3 Processed Bucket: {CONFIG['aws']['s3_processed_bucket']}")