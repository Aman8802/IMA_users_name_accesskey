import json
import boto3

from datetime import datetime, timedelta


def lambda_handler(event, context):
    session = boto3.Session(aws_access_key_id="AKIA**************",aws_secret_access_key="hiZ2pp+****************")
    
    resource = session.resource('iam')
    client = session.client('iam')
    

    list_of_objects = []
    for user in resource.users.all():
        Metadata = client.list_access_keys(UserName = user.user_name)
        LastUserUsed = user.password_last_used
        if Metadata['AccessKeyMetadata'] :
            list_of_keys = []
            for key in user.access_keys.all():
                AccessKeyId = key.access_key_id
                if(client.get_access_key_last_used(AccessKeyId=AccessKeyId)['AccessKeyLastUsed']['ServiceName'] == "N/A"):
                    LastUsedAccessKey = "N/A"
                else:
                    LastUsedAccessKey = client.get_access_key_last_used(AccessKeyId=AccessKeyId)['AccessKeyLastUsed']['LastUsedDate']
                    lastActivity = datetime.now(LastUsedAccessKey.tzinfo) - LastUsedAccessKey          
                    SinceLastUsedAccessKeyDays = lastActivity.days
                list_of_keys.append({"Access_key_id":AccessKeyId,"LastUsedAccessKey":LastUsedAccessKey,"SinceLastUsedAccessKey": SinceLastUsedAccessKeyDays})
            list_of_objects.append({"UserName":user.user_name,"Access_Keys": list_of_keys})
        else:
            print("User dont have AccessKey")     


    print(list_of_objects)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
