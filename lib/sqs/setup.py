from boto import sqs
import os

class SQSConnection:
	def __init__(self):
		# Get the parameters
		params = {}
		params['aws_access_key_id'] = os.environ["AWS_ACCESS_KEY_ID"]
		params['aws_secret_access_key'] = os.environ["AWS_SECRET_KEY"]

		self.conn = sqs.connect_to_region('us-east-1', **params)

SQS_Manager = SQSConnection()