import boto3
import pandas as pd
from sqlalchemy import create_engine
import json
import time
import os
from etl.utils import handle_null_values, validate_schema, validate_foreign_keys
from etl.logger import logger
from etl.config import DB_PARAMS, NULL_DATE_PLACEHOLDER

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

def create_db_engine():
    return create_engine(f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}")

def process_s3_file(bucket, key, engine):
    logger.info(f"Processing file {key} from bucket {bucket}")
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(response['Body'])
        
        table_name = key.split('/')[-1].split('.')[0]
        logger.info(f"Identified table name: {table_name}")

        df = handle_null_values(df, table_name)
        df = validate_schema(df, table_name, engine)
        
        if table_name == 'hired_employees':
            df = validate_foreign_keys(df, engine, 
                                       {'department_id': 'departments', 'job_id': 'jobs'})

        df.to_sql(table_name, engine, if_exists='append', index=False)
        logger.info(f"Successfully loaded {len(df)} rows into {table_name}")

    except Exception as e:
        logger.error(f"Error processing file {key}: {str(e)}")

def aws_etl_process():
    logger.info("Starting AWS ETL process")
    engine = create_db_engine()
    queue_url = os.environ.get('sqs_queue_url')
    
    if not queue_url:
        logger.error("SQS_QUEUE_URL environment variable not set")
        return

    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )
            
            if 'Messages' in response:
                for message in response['Messages']:
                    body = json.loads(message['Body'])
                    event = json.loads(body['Message'])
                    
                    for record in event['Records']:
                        bucket = record['s3']['bucket']['name']
                        key = record['s3']['object']['key']
                        process_s3_file(bucket, key, engine)
                    
                    # Delete the message from the queue
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
            else:
                logger.info("No messages in queue, waiting...")
                time.sleep(60)
        except Exception as e:
            logger.error(f"Error in ETL process: {str(e)}")
            time.sleep(60)  # Wait a bit before retrying

if __name__ == "__main__":
    aws_etl_process()