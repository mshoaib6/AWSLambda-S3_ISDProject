import json
import boto3
import urllib
from pprint import pprint

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('celebrities')
    
    response = table.scan(
        ProjectionExpression="filename, celebrities"
    )
    
    result = {}
    
    if event['queryStringParameters'] is None:
        for item in response['Items']:
            for this_item in item['celebrities']:
                        
                this_item_filename = item['filename']
                this_item_confidence = float(this_item['confidence'])
                this_item_urls = this_item['Urls']
                this_item_id = this_item['id']
                        
                this_dict = {
                    "filename": this_item_filename,
                    "confidence": this_item_confidence,
                    "Urls": this_item_urls,
                    "id": this_item_id
                }
                
                if this_item['name'] not in result.keys():
                    this_celeb = []
                    dict_key = this_item['name']
                    this_celeb.append(this_dict)
                    result[dict_key] = this_celeb
                    
                elif this_item['name'] in result.keys():
                    this_celeb = []
                    dict_key = this_item['name']
                    this_celeb = result[dict_key]
                    this_celeb.append(this_dict)
                    this_celeb.sort(key=lambda item: item.get("filename"))
                    result[dict_key] = this_celeb
    
    elif 'queryStringParameters' in event and 'conf' in event['queryStringParameters']:
        compare_conf = event['queryStringParameters']['conf']
        for item in response['Items']:
            for this_item in item['celebrities']:
                this_item_confidence = float(this_item['confidence'])
                
                if this_item_confidence >= float(compare_conf):
                    
                    this_item_filename = item['filename']
                    this_item_urls = this_item['Urls']
                    this_item_id = this_item['id']
                        
                    this_dict = {
                        "filename": this_item_filename,
                        "confidence": this_item_confidence,
                        "Urls": this_item_urls,
                        "id": this_item_id
                    }
                
                    if this_item['name'] not in result.keys():
                        this_celeb = []
                        dict_key = this_item['name']
                        this_celeb.append(this_dict)
                        result[dict_key] = this_celeb
                        
                    elif this_item['name'] in result.keys():
                        this_celeb = []
                        dict_key = this_item['name']
                        this_celeb = result[dict_key]
                        this_celeb.append(this_dict)
                        this_celeb.sort(key=lambda item: item.get("filename"))
                        result[dict_key] = this_celeb
    
        
        
        
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
