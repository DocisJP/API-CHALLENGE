import json
import boto3
import csv
from io import StringIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        csv_file = StringIO(file_content)
        csv_reader = csv.reader(csv_file)
        
        # Perform validation (e.g., check number of columns, data types)
        # This is a simple example; you should implement more robust validation
        for row in csv_reader:
            if len(row) != 5:  # Assuming 5 columns in the CSV
                raise ValueError("Invalid number of columns")
        
        # If validation passes, move file to processed bucket
        s3.copy_object(
            Bucket='globant-processed-data',
            CopySource={'Bucket': bucket, 'Key': key},
            Key=key
        )
        s3.delete_object(Bucket=bucket, Key=key)
        
        return {
            'statusCode': 200,
            'body': json.dumps('File validated and moved successfully')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing the file')
        }