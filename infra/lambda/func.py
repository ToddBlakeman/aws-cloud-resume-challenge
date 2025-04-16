"""
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
    return views"""

import json
import boto3
from datetime import datetime

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Specify the table
table = dynamodb.Table('view-count-ddb')

# Set up SES client for email notifications
ses_client = boto3.client('ses')

def send_email(subject, body):
    # Replace with your SES verified email addresses
    response = ses_client.send_email(
        Source='your-email@example.com',  # Verified sender
        Destination={
            'ToAddresses': ['your-email@example.com'],  # Replace with your email
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': body
                }
            }
        }
    )

def lambda_handler(event, context):
    # Fetch the item with 'id' = '0' from DynamoDB
    response = table.get_item(Key={'id': '0'})
    
    # Extract and increment the views count
    views = response['Item']['views']
    views += 1
    print(f"Updated view count: {views}")
    
    # Update the DynamoDB table with the new views count
    table.put_item(Item={
        'id': '0',  # Assuming you are updating the same item
        'views': views
    })
    
    # Get the current timestamp
    timestamp = datetime.utcnow().isoformat()
    
    # Log the visit event in CloudWatch Logs
    log_message = f"Website visited at: {timestamp} | New views count: {views}"
    print(log_message)  # This will log to CloudWatch automatically
    
    # Send an email notification (optional)
    send_email("Website Visit Notification", log_message)
    
    # Return the updated views count
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Visit logged, view count updated, and email sent.',
            'views': views
        })
    }
