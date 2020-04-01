import json
import boto3
import os

def lambda_handler(event, context):
    # TODO implement
    cognito = boto3.client('cognito-idp')
    print("What does this get me??? ... {} ".format(event))
    username=event['userName']
    provider=""
    email=""
    
    try:
        identities = json.loads(event['request']['userAttributes']['identities'])
        provider = identities[0]['providerName']
        print("Provider: {}".format(provider))
    except:
        print('No provider')
    try:
        email= event['request']['userAttributes']['email']
        print("Email: {}".format(email))
    except:
        print('No email???')

    if provider=="Google" and "@urbanevo.com" in email:
        print("Adding {} to admin group".format(email))
        cognito.admin_add_user_to_group(UserPoolId= os.environ['COGNITO_POOL']
                                        ,Username=username
                                        ,GroupName=os.environ['ADMIN_GROUP']
                                        )
    return event
