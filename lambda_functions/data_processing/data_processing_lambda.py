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
        
        # Process the data (e.g., transform, aggregate)
        # This is where you'd implement your data processing logic
        processed_data = []
        for row in csv_reader:
            # Example: Capitalize all strings in the row
            processed_row = [item.upper() for item in row]
            processed_data.append(processed_row)
        
        # Write processed data back to S3
        output = StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerows(processed_data)
        
        s3.put_object(
            Bucket='globant-processed-data',
            Key=f"processed_{key}",
            Body=output.getvalue()
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data processed successfully')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing the data')
        }