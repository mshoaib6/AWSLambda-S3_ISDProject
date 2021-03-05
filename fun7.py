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
    
    searched_name = event['pathParameters']['name']
    searched_name = searched_name.replace("%20", " ")
    
    if event['queryStringParameters'] is None:
        resultList = []
        for item in response['Items']:
            
            found = False
            for this_item in item['celebrities']:
                if this_item['name'] == searched_name:
                    found = True
                    
                    this_item_filename = item['filename']
                    this_celebrity_name = this_item['name']
                    this_item_confidence = float(this_item['confidence'])
                    this_item_urls = this_item['Urls']
                    this_item_id = this_item['id']
                            
                    this_dict = {
                        "filename": this_item_filename,
                        "celebrity_name": this_celebrity_name,
                        "confidence": this_item_confidence,
                        "Urls": this_item_urls,
                        "id": this_item_id
                    }
                    
                    resultList.append(this_dict)
        
        resultList.sort(key=lambda item: item.get("filename"))
                    
        if found == True:
            result = {
                "files" : resultList
            }
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        else:
            result = {
                "Error":"Celebrity not found"
            }
            return {
                'statusCode': 404,
                'body': json.dumps(result)
            }
            
    elif 'queryStringParameters' in event and 'conf' in event['queryStringParameters']:
        
        compare_conf = event['queryStringParameters']['conf']
        resultList = []
        for item in response['Items']:
            
            found = False
            for this_item in item['celebrities']:
                this_item_confidence = float(this_item['confidence'])
                
                if this_item['name'] == searched_name :
                    found = True
                    
                    if this_item_confidence>= float(compare_conf):
                    
                        this_item_filename = item['filename']
                        this_celebrity_name = this_item['name']
                        
                        this_item_urls = this_item['Urls']
                        this_item_id = this_item['id']
                                
                        this_dict = {
                            "filename": this_item_filename,
                            "celebrity_name": this_celebrity_name,
                            "confidence": this_item_confidence,
                            "Urls": this_item_urls,
                            "id": this_item_id
                        }
                        
                        resultList.append(this_dict)
        
        resultList.sort(key=lambda item: item.get("filename"))
                    
        if found == True:
            result = {
                "files" : resultList
            }
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        else:
            result = {
                "Error":"Celebrity not found"
            }
            return {
                'statusCode': 404,
                'body': json.dumps(result)
            }
                    
                
    




