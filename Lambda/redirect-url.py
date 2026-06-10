import boto3

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-shortener')

def lambda_handler(event, context):

    try:
        short_id = event['pathParameters']['id']

        response = table.get_item(
            Key={
                'short_id': short_id
            }
        )

        item = response.get('Item')

        if not item:
            return {
                'statusCode': 404,
                'body': 'URL not found'
            }

        return {
            'statusCode': 302,
            'headers': {
                'Location': item['long_url']
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }