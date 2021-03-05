import json

def lambda_handler(event, context):
    # TODO implement
    
    result = {
        "id": "18079999D",
        "name": "Shoaib Muhammad"
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
