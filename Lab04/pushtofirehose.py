import boto3
import json
import pandas as pd

# Initialize a boto3 client for Firehose
firehose_client = boto3.client(
    'firehose',
    aws_access_key_id='AKIAWMFUPOMUFYQENSMI',
    aws_secret_access_key='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',
    region_name='us-east-1',
)
# Define the Firehose stream name
firehose_stream_name = 'VehicleDataFHStream'
data_path = "vehicle2.csv"

# Sample data to push to Firehose stream
df = pd.read_csv(data_path)
for index,row in df.iterrows():
    # Create a JSON payload from the row data
    payload = json.dumps(row.to_dict())
    vehicle_data_json = payload
    # print(vehicle_data_json)
    # print(row.values)
    # Push data to Firehose stream
    response = firehose_client.put_record(
        DeliveryStreamName=firehose_stream_name,
        Record={
            'Data': vehicle_data_json   # Add newline character to each record
        }
    )
    print(response)

# import csv

# with open(data_path, 'r') as file:
#     csv_reader = csv.reader(file)
#     for row in csv_reader:
#         print(row)

# Print response from Firehose
# print(vehicle_data_json)