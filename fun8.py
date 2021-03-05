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
    
    if event['queryStringParameters'] is None:
    
        resultList = []
        thisList = []
        
        for item in response['Items']:
            thisFileDict = {}
            list = []
            for this_item in item['celebrities']:
                
                this_item_confidence = float(this_item['confidence'])
                this_item_urls = this_item['Urls']
                this_item_id = this_item['id']
                this_item_name = this_item['name']
                
                this_dict = {
                    "confidence": this_item_confidence,
                    "name": this_item_name,
                    "Urls": this_item_urls,
                    "id": this_item_id
                }
                thisList.append(this_dict)
            thisList.sort(key=lambda item: item.get("name"))
            this_item_filename = item['filename']
            thisFileDict = {
                "filename": this_item_filename,
                "celebrities": thisList
            }
            
            resultList.append(thisFileDict)
            thisList =[]
        resultList.sort(key=lambda item: item.get("filename"))
        
        return {
            'statusCode': 200,
            'body': json.dumps(resultList)
        }
    
    elif 'queryStringParameters' in event and 'conf' in event['queryStringParameters']:
        compare_conf = event['queryStringParameters']['conf']
        resultList = []
        thisList = []
        
        for item in response['Items']:
            thisFileDict = {}
            list = []
            for this_item in item['celebrities']:
                
                this_item_confidence = float(this_item['confidence'])
                
                if this_item_confidence >= float(compare_conf):
                
                    this_item_urls = this_item['Urls']
                    this_item_id = this_item['id']
                    this_item_name = this_item['name']
                    
                    this_dict = {
                        "confidence": this_item_confidence,
                        "name": this_item_name,
                        "Urls": this_item_urls,
                        "id": this_item_id
                    }
                    thisList.append(this_dict)
                    
            thisList.sort(key=lambda item: item.get("name"))
            this_item_filename = item['filename']
            thisFileDict = {
                "filename": this_item_filename,
                "celebrities": thisList
            }
            
            resultList.append(thisFileDict)
            thisList =[]
        resultList.sort(key=lambda item: item.get("filename"))
        
        return {
            'statusCode': 200,
            'body': json.dumps(resultList)
        }