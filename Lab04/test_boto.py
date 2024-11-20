import boto3

client = boto3.client(
    's3',
    aws_access_key_id='AKIAWMFUPOMUFYQENSMI',
    aws_secret_access_key='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',
)

print(client.list_buckets())