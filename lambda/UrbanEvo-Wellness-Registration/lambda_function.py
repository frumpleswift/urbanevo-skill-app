import json

import re
import os
from botocore.vendored import requests
import traceback
import hashlib
import boto3
import datetime
import os
import io
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from botocore.exceptions import ClientError
from lxml import html


def verifyEmail(email):

    session = requests.Session()
    r = session.get(
        'https://www.wellnessliving.com/selfsignup/37RrPjmtY', timeout=5)

    tree = html.fromstring(r.text.replace('\\', ''))

    controller = tree.xpath("//script[contains(.,'Ajax._startup')]/text()")
    ajaxID = str(controller[0]).split("'")[1]

    emailData = {'a-ajax': ajaxID, 'a_data[id_place]': '4', 'a_data[s_mail]': email, 'a_data[uid_current]': 0, 'a_data[s_secret]': '37RrPjmtY', 's_method': 'Wl\Login\Add\Ajax::mailVerifyPrompt'
                 }

    r = session.post("https://www.wellnessliving.com/a/ajax.html",
                     data=emailData, timeout=10)

    print("In verify: {}".format(r.text))

    return r.text



def lambda_handler(event, context):

    content = json.loads(event['body'])

    # request info
    status = 200
    method = event.get('httpMethod')

    try:

        checkEmail = verifyEmail(content["email"])
        if "s_message" in checkEmail or "already" in checkEmail:
            ret = {"error": "Email Address Already Registered"}
            status = 400
        else:

            #first save the information to dynamo
            dynamodb = boto3.client('dynamodb')
            table_name = os.environ["WELLNESS_TABLE"]
            crud_time=str(int(datetime.datetime.now().timestamp()))
            email=content["email"]
            # serializers to convert dict to dynamodb map and back
            serializer = TypeSerializer()
            deserializer = TypeDeserializer()

            toStore={k: v for k, v in content.items() if (v is not None and v != '')}
            the_password=toStore.pop("pwd",None)

            serialized = serializer.serialize(toStore)
            print(email,crud_time,serialized)
            response = dynamodb.put_item(TableName=table_name,Item={"email":{"S":email},"crud_time":{"N":crud_time},"user_data":serialized})

            #push SNS notification of registration event
            # Create an SNS client
            sns = boto3.client('sns')
            response = sns.publish(
                TopicArn='arn:aws:sns:us-east-1:748492294422:UrbanEvo-Wellness-Registration-Event',
                Message=json.dumps({"the_email":email,"the_time":crud_time,"the_other":the_password}),
                )

            #finished processing
            status = 200
            ret = {"success":"Registration information received!"}

    except Exception as e:
        #traceback.print_stack()
        ret = {"error":str(e)}
        status = 400
        print(e)

    return {
        'statusCode': status,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(ret)
    }
