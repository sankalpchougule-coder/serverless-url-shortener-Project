import json
import boto3
import random
import string

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-shortener')

# Generate random short ID
def generate_short_id():
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=6
        )
    )

def lambda_handler(event, context):

    try:
        body = json.loads(event['body'])

        long_url = body['url']

        short_id = generate_short_id()

        table.put_item(
            Item={
                'short_id': short_id,
                'long_url': long_url
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'short_id': short_id
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }