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