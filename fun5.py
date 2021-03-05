import json
import boto3
import urllib
from pprint import pprint

def lambda_handler(event, context):
    
    celeb_list = []
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('celebrities')
    
    response = table.scan(
        ProjectionExpression="celebrities"
    )
    
    for item in response['Items']:
        for this_item in item['celebrities']:
            if this_item['name'] not in celeb_list:
                celeb_list.append(this_item['name'])
    
    celeb_list.sort()
    
    result = {
        "celebrities_names":celeb_list
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
