import json
import boto3
import time
import decimal
import datetime

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

# 連番を裁判して返す関数
def get_next_seq(table, tablename):
	response = table.update_item(
		Key = {
			'tablename' : tablename
		},
		UpdateExpression='set seq = seq + :val',
		ExpressionAttributeValues = {
			':val' : 1
		},
		ReturnValues='UPDATED_NEW'
	)
	return response['Attributes']['seq']

def lambda_handler(event, context):
	try:
		## フォームに入力されたデータを得る
		param = json.loads(event['body'])
		email = param['email']
		
		# user テーブルからemailで検索。idを取得
		user_table = dynamodb.Table( 'user' )
		user = user_table.get_item( Key = { 'email' : email } )
		
		if user.get("Item") is None:
			# 初回登録の場合シーケンスデータを得る
			seqtable = dynamodb.Table('sequence')
			nextseq = get_next_seq(seqtable, 'user')
			
			# user テーブルに登録する
			user_table.put_item(
				Item = {
					'email' : email,
					'id' : nextseq
				}
			)
			
			# basicprofile テーブルに登録する。
			bp_table = dynamodb.Table('basicprofile')
			bp_table.put_item(
				Item = {
					'user_id' : nextseq,
					# 'birthday' : birthday,
					# 'direction' : direction,
					# 'educational_background' : educational_background,
					# 'experience' : experience,
					# 'like' : like,
					# 'name' : name,
					# 'publishing_setting' : publishing_setting,
					# 'self_introduction' : self_introduction,
					# 'skill' : skill,
					# 'telephone_number' : telephone_number,
					# 'work_history' : work_history
				}
			)
			
			# gamerprofile テーブルに登録する。
			gp_table = dynamodb.Table('gamerprofile')
			gp_table.put_item(
				Item = {
					'user_id' : nextseq,
					# 'delivery_platform' : delivery_platform,
					# 'game_title' : game_title,
					# 'good_at' : good_at,
					# 'history' : history,
					# 'play_style' : play_style,
					# 'player_name' : player_name,
					# 'position' : position,
					# 'proud' : proud,
					# 'publishing_setting' : publishing_setting,
					# 'rank' : rank,
					# 'twitter' : twitter,
					# 'url' : url,
					# 'youtube' : youtube
				}
			)
		else:
			# ユーザIDを取得
			user_id = user[ "Item" ][ "id" ]
		
			# 編集
			# basicprofile テーブルを更新する
			bp_table = dynamodb.Table('basicprofile')
			response = bp_table.update_item(
				Key = {
					'user_id' : user_id
				},
				UpdateExpression = 'set work_history = :work_history',
				ExpressionAttributeValues = {
					# 'birthday' : birthday,
					# 'direction' : direction,
					# 'educational_background' : educational_background,
					# 'experience' : experience,
					# 'like' : like,
					# 'name' : name,
					# 'publishing_setting' : publishing_setting,
					# 'self_introduction' : self_introduction,
					# 'skill' : skill,
					# 'telephone_number' : telephone_number,
					':work_history' : '2018～'
				},
				ReturnValues='UPDATED_NEW'
			)
			
			# gamerprofile テーブルを更新する
			gp_table = dynamodb.Table('gamerprofile')
			response = gp_table.update_item(
				Key = {
					'user_id' : user_id
				},
				UpdateExpression = 'set youtube = :youtube',
				ExpressionAttributeValues = {
					# 'delivery_platform' : delivery_platform,
					# 'game_title' : game_title,
					# 'good_at' : good_at,
					# 'history' : history,
					# 'play_style' : play_style,
					# 'player_name' : player_name,
					# 'position' : position,
					# 'proud' : proud,
					# 'publishing_setting' : publishing_setting,
					# 'rank' : rank,
					# 'twitter' : twitter,
					# 'url' : url,
					':youtube' : 'なし'
				},
				ReturnValues='UPDATED_NEW'
			)
		
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
		    "body": json.dumps({"result":email})
		}

	except:
		import traceback
		traceback.print_exc()
		return {
			'statusCode' : 500
		}
