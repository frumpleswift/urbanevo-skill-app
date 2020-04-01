import json
import boto3
import uuid
import base64
import datetime
import os
import io
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    #request info
    method = event.get('httpMethod')
    user_id = guid = event.get('pathParameters').get('user_id')
    skill = guid = event.get('pathParameters').get('skill')  
    
    #hacky authentication
    try:
        
        groups = event['requestContext']['authorizer']['claims']['cognito:groups']
        sub_id = event['requestContext']['authorizer']['claims']['sub']
        
    except Exception as exc:
        print(exc)
        return {
                'statusCode': 401,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': '{"error":"error retrieving authentication context"}'
            }
            
    if sub_id != user_id and os.environ['AUTH_GROUP'] not in groups:
        return {
            'statusCode': 401,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': '{"error":"access denied"}'
        }

    #get dynamo table info 
    dynamodb = boto3.client('dynamodb')
    table_name = os.environ["PROFILE_TABLE"]
    record_name = skill + "_progress"
    
    #serializers to convert dict to dynamodb map and back
    serializer = TypeSerializer()
    deserializer = TypeDeserializer()
    
    #the time
    crud_time=str(int(datetime.datetime.now().timestamp()))
         
    if method=="GET":
        #to do
        record = dynamodb.get_item(TableName=table_name,Key={"user_id":{"S":user_id}})
        deserialized = deserializer.deserialize(record.get('Item').get(record_name))
        ret = {"user_id":user_id,"skill":skill,"skill_data":deserialized}   
        
    if method=="PUT":
        
        rec = json.loads(event['body'])
        serialized = serializer.serialize(rec)
        
        update_expression = 'SET ' + record_name + ' = :a, crud_time = :b'
        
        response = dynamodb.update_item(TableName=table_name
                                       ,Key={"user_id":{"S":user_id}}
                                       ,UpdateExpression=update_expression
                                       ,ExpressionAttributeValues = {':a':serialized,':b':{"N":crud_time}})
                                       
        ret = {"user_id":user_id,"updated":skill,"time":crud_time}
            
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(ret)
    }
