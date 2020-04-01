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
    
    #hacky protection on put and delete
    if event['httpMethod'] in ['PUT','DELETE']:
        try:
        
            groups = event['requestContext']['authorizer']['claims']['cognito:groups']
        
            if os.environ['AUTH_GROUP'] not in groups:
                return {
                    'statusCode': 401,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': '{"error":"access denied"}'
                }
        except Exception as exc:
            print(exc)
            return {
                    'statusCode': 401,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': '{"error":"error retrieving authentication context"}'
                }
    
    #get dynamo client
    dynamodb = boto3.client('dynamodb')
    
    #serializers to convert dict to dynamodb map and back
    serializer = TypeSerializer()
    deserializer = TypeDeserializer()
    
    crud_time=str(int(datetime.datetime.now().timestamp()))
    
    method = event.get('httpMethod')
    record_name = event.get('pathParameters').get('record-name')
    guid = event.get('pathParameters').get('uuid')
    status = 200
    
    table_name = 'SkillApp-{}-Records'.format(record_name)

    if method == 'GET':
        if guid:
            
            record = dynamodb.get_item(TableName=table_name,Key={"guid":{"S":guid}})
            deserialized = deserializer.deserialize(record.get('Item').get("record_data"))
            ret = {"guid":guid,"record_data":deserialized}        
            
        else:
            
            records = dynamodb.scan(TableName=table_name
                                   ,Select='SPECIFIC_ATTRIBUTES'
                                   ,ProjectionExpression='guid')
            try:
                record_list=[]
                for rec in records.get('Items'):
                    record_list.append(rec.get("guid").get("S"))
            except AttributeError:
                status=404
                record_list=["No records found"]
            
            ret = record_list
        
    if method == 'PUT':
        
        action="updated"
        
        rec = json.loads(event['body'])
        
        if not guid:
            action="created"
            
        oldguid = guid
        guid = ''.join(e for e in rec.get("name") if e.isalnum()).lower()  #str(uuid.uuid4())
        
        #hacky duplicate prevention
        if action=="created" or oldguid != guid:
            #check for dupes
            record = dynamodb.get_item(TableName=table_name,Key={"guid":{"S":guid}})
            print(record)
            if "Item" in record:
                print("ERROR: Key already exists")
                return {
                    'statusCode': 400,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': '{"status":0,"statusText":"error","error":"Record Already Exists"}'
                    }
                    
        #process an upload if it exists
        if "upload" in rec:
            image = rec.pop("upload").split(",")
            
            content = image[0]
            contentType = content.split(";")[0].split(":")[1]
            b64 = image[1]
            #acl='public-read'
            
            name = rec.get("image_name")
            bytes = base64.b64decode(b64)
            file = io.BytesIO(bytes)   
            s3 = boto3.client('s3')
            s3.upload_fileobj(file, os.environ["image_bucket"], name)
        
            rec["image_url"] = "{}://{}/{}".format(os.environ["protocol"],os.environ["image_bucket"],name)
        
        serialized = serializer.serialize(rec)
        
        response = dynamodb.update_item(TableName=table_name
                                       ,Key={"guid":{"S":guid}}
                                       ,UpdateExpression='SET record_data = :a, crud_time = :b'
                                       ,ExpressionAttributeValues = {':a':serialized,':b':{"N":crud_time}})
        ret = {"guid":guid,"action":action,"time":crud_time}
        
    if method == 'DELETE':
        ret = {}
    
        try:
            
            dynamodb.delete_item(TableName=table_name,Key={"guid":{"S":guid}})
            ret = {"action": "delete", "status":"deleted","guid":guid}
            
        except Exception as ex:
            
            status = 400
            ret: {"action":"delete","status":"failed","error":str(ex)}
    
    return {
            'statusCode': status,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(ret)
        }
    
    
    
    
