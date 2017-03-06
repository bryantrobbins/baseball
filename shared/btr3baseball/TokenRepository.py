import boto3
import uuid

class TokenRepository:
    def __init__(self, tokenTable):
        self.table = boto3.resource('dynamodb').Table(tokenTable)
        
    def getToken(self, keyId):
        try:
            response = self.table.get_item(
                Key={
                    'keyid': keyId
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
        else:
            item = response['Item']
            return item

