import json
import boto3
import urllib

def lambda_handler(event, context):
    
    images_list = []
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('celebrities')
    
    response = table.scan(
        ProjectionExpression="filename"
    )
    
    for item in response['Items']:
        images_list.append(item['filename'])
        
    result = {
        "images": images_list
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
