import json
import boto3
import decimal

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, decimal.Decimal):
           return int(obj)
       return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
	try:
		#param = event['data']
		#date = param['email']
		param = event.get('queryStringParameters')
		email = param['email']
		
		# user テーブルからemailで検索
		user_table = dynamodb.Table( 'user' )
		user = user_table.get_item( Key = { 'email' : email } )
		
		user_id = user[ "Item" ][ "id" ]
	
		basic_profile = dynamodb.Table( 'basicprofile' )
		basicprofile = basic_profile.get_item( Key = { 'user_id' : user_id } )
		
		gamer_pdofile = dynamodb.Table('gamerprofile')
		gamerprofile = gamer_pdofile.get_item( Key = { 'user_id' : user_id } )
		
		result = {
			"BP" : basicprofile[ "Item" ],
			"GP" : gamerprofile[ "Item" ]
		}
		
		# 結果を返す
		return {
			    "isBase64Encoded": False,
			    "statusCode": 200,
			    "headers": {
			        'Content-Type': 'application/json',
			        'Access-Control-Allow-Headers': 'Content-Type',
			        'Access-Control-Allow-Methods': 'POST,GET',
			        'Access-Control-Allow-Origin': '*'
    			},
			    "body": json.dumps(result, cls=DecimalEncoder)
		}

	except:
		import traceback
		traceback.print_exc()
		return {
			'statusCode' : 500
		}