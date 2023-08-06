import os
import json
from .lambda_executor import LambdaExecutor
from .s3_operations import S3Operations
from .dynamo_operations import DynamoOperations

input_bucket = os.environ['INPUT_BUCKET']  # TODO: move some of these variables to be passed in from SNS
output_bucket = os.environ['OUTPUT_BUCKET']
table_name = os.environ['TABLE_NAME']
#
output_bucket_access_key = os.environ['OUTPUT_BUCKET_ACCESS_KEY']
output_bucket_secret_access_key = os.environ['OUTPUT_BUCKET_SECRET_ACCESS_KEY']

# executor = LambdaExecutor(
#     s3_operations=S3Operations(),
#     dynamo_operations=DynamoOperations(),
#     #
#     # input_bucket=input_bucket, # TODO: remove
#     # output_bucket=output_bucket,
#     # table_name=table_name,
#     #
#     output_bucket_access_key=output_bucket_access_key,
#     output_bucket_secret_access_key=output_bucket_secret_access_key
# )
executor = LambdaExecutor(
    S3Operations(),
    DynamoOperations(),
    input_bucket,
    output_bucket,
    table_name,
    output_bucket_access_key,
    output_bucket_secret_access_key
)


def handler(sns_event, context):
    print("Event : " + str(sns_event))
    print("Context : " + str(context))
    # This should only ever be one message at a time...
    for record in sns_event['Records']:
        message = json.loads(record['Sns']['Message'])
        print("Start Message : " + str(message))
        executor.execute(message)
        print("Done Message : " + str(message))
    print("Done Event : " + str(sns_event))
