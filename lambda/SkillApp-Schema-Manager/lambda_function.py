import json
import boto3
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
import botocore
import os

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
    
    dynamodb = boto3.client('dynamodb')
    record_name=event['path'].strip("/")
    
    #serializers to convert dict to dynamodb map and back
    serializer = TypeSerializer()
    deserializer = TypeDeserializer()
    
    if event['httpMethod'] == 'GET':
        if record_name == "":
            records = dynamodb.scan(TableName='SkillApp-Record-Schemas'
                                   ,Select='SPECIFIC_ATTRIBUTES'
                                   ,ProjectionExpression='record_name,img_url')
            status=200
            #record_list = deserializer.deserialize(records.get('Items'))
            try:
                record_list=[]
                for rec in records.get('Items'):
                    item = {"record_name":rec.get("record_name").get("S")}
                    try:
                        item["img_url"] = rec.get("img_url").get("S")
                    except AttributeError:
                        pass
                    record_list.append(item)
            except AttributeError:
                status=404
                record_list=["No records found"]
            return {
                'statusCode': status,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps(record_list)
            }
        
        record = dynamodb.get_item(TableName='SkillApp-Record-Schemas',Key={"record_name":{"S":record_name}})
        status=200
        try:
            record_schema = json.dumps(deserializer.deserialize(record.get('Item').get("record_schema")))
        except AttributeError:
            status=404
            record_schema="Record {} not found".format(record_name)
        
        return {
            'statusCode': status,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': record_schema
        }
    if event['httpMethod'] == 'PUT':
        
        schema = json.loads(event['body'])
        serialized = serializer.serialize(schema)
        
        response = dynamodb.update_item(TableName='SkillApp-Record-Schemas'
                                       ,Key={"record_name":{"S":record_name}}
                                       ,UpdateExpression='SET record_schema = :a, img_url= :b'
                                       ,ExpressionAttributeValues = {':a':serialized, ':b':{"S":schema.get("img_url")}})
                  
        try:                               
            new_table = dynamodb.create_table(TableName='SkillApp-{}-Records'.format(record_name)
                                         ,AttributeDefinitions=[{'AttributeName':'guid','AttributeType':'S'}]
                                         ,KeySchema=[{'AttributeName':'guid','KeyType':'HASH'}]
                                         ,ProvisionedThroughput={'ReadCapacityUnits': 5
                                                                ,'WriteCapacityUnits': 5}
                                         )
        except dynamodb.exceptions.ResourceInUseException as exc:
            pass
            
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': "{} successfully updated".format(record_name)
        }
    if event['httpMethod'] == 'DELETE':
        response = dynamodb.delete_item(TableName='SkillApp-Record-Schemas',Key={"record_name":{"S":record_name}})
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': "{} successfully deleted".format(record_name)
        }
    
    raise Exception("Method {} not implemented".format(event['httpMethod']))
    
    
