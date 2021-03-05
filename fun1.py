import json
import boto3
import urllib
from decimal import *

rekognition_client=boto3.client('rekognition')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('celebrities')

def recognize_celebrities(bucket, key):
    response = rekognition_client.recognize_celebrities(
        Image={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    return response

def lambda_handler(event, context):
    
    r = event['Records'][0]
    key = urllib.parse.unquote_plus(r['s3']['object']['key'], encoding='utf-8')
    
    event_name = r['eventName']
    bucket="polyu-comp3122a2-18079999d"
    
    if event_name == "ObjectCreated:Put":
        listOfCelebs =[]
        r = recognize_celebrities(bucket, key)
        
        
        for celebrity in r['CelebrityFaces']:
            thisCelebDict = {
                "confidence": Decimal(celebrity['MatchConfidence']),
                "id": celebrity['Id'],
                "name": celebrity['Name'],
                "Urls": celebrity['Urls']
            } 
            
            dictCopy = thisCelebDict.copy()
            listOfCelebs.append(dictCopy)
        

        table.put_item(
            Item = {
                "filename" : key,
                "celebrities" : listOfCelebs
            }
        )

    if event_name == "ObjectRemoved:Delete":
        table.delete_item(
            Key={
                "filename" : key
            }
        )
