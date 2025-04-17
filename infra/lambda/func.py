import json
import boto3

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Specify the table
table = dynamodb.Table('view-count-ddb')

def lambda_handler(event, context):
    # Fetch the item with 'id' = '0'
    response = table.get_item(Key={'id': '0'})
    
    # Extract and increment the views count
    views = response['Item']['views']
    views += 1
    print(views)
    
    # Update the item with new views count
    table.put_item(Item={
        'id': '0',  # Assuming you meant to update the same item
        'views': views
    })
    
    # Return the updated views count
    return views





""" TEST CODE
import json
import boto3
from datetime import datetime

# Initialize S3 client
s3_client = boto3.client('s3')

# S3 bucket name
bucket_name = 'website-visit-logs-8375'  # Replace with your S3 bucket name

# Specify the view count table
dynamodb = boto3.resource('dynamodb')
views_table = dynamodb.Table('view-count-ddb')  # Replace with your views table name

def lambda_handler(event, context):
    # Fetch the item with 'id' = '0' from DynamoDB (view count table)
    response = views_table.get_item(Key={'id': '0'})
    
    # Extract and increment the views count
    views = response['Item']['views']
    views += 1
    print(f"Updated view count: {views}")
    
    # Update the view count table with the new views count
    views_table.put_item(Item={
        'id': '0',  # Assuming you are updating the same item
        'views': views
    })
    
    # Get the current timestamp
    timestamp = datetime.utcnow().isoformat()
    
    # Prepare the log message
    log_message = {
        'timestamp': timestamp,
        'views_count': views
    }
    
    # Create a log entry as a JSON object
    log_json = json.dumps(log_message)
    
    # Generate the file name using the timestamp
    file_name = f"visit-log-{timestamp}.json"
    
    # Store the log in the S3 bucket
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=log_json,
        ContentType='application/json'
    )
    
    # Log the visit event in CloudWatch Logs
    print(f"Website visited at: {timestamp} | New views count: {views}")
    
    # Return the updated views count
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Visit logged and view count updated.',
            'views': views
        })
    }
"""
