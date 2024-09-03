import json
import boto3
import csv
from io import StringIO

s3 = boto3.client('s3')

def validate_csv(rows, expected_columns):
    if len(rows[0]) != expected_columns:
        raise ValueError(f"CSV should have {expected_columns} columns")
    # Add more specific validations as needed

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        csv_file = StringIO(file_content)
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)
        
        if key.startswith('departments'):
            validate_csv(rows, 2)
        elif key.startswith('jobs'):
            validate_csv(rows, 2)
        elif key.startswith('hired_employees'):
            validate_csv(rows, 5)
        else:
            raise ValueError(f"Unexpected file: {key}")
        
        # If validation passes, move file to processed bucket
        s3.copy_object(
            Bucket='globant-processed-data',
            CopySource={'Bucket': bucket, 'Key': key},
            Key=key
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('File validated and moved successfully')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing the file: {str(e)}')
        }