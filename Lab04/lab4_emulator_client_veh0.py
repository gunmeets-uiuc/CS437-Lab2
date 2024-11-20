
# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from datetime import datetime
import json
import pandas as pd
import numpy as np
import logging

# from awsgreengrasspubsubsdk.pubsub_client import AwsGreengrassPubSubSdkClient

from awsgreengrasspubsubsdk.message_formatter import PubSubMessageFormatter
formatter = PubSubMessageFormatter()



#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 10
device_end = 19

#Path to the dataset, modify this
data_path = "vehicle1_test.csv"

#Path to your certificates, modify this
# certificate_formatter = "certificate.pem"
# key_formatter = "device.private.pem"


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("avsk2qeejl1gz-ats.iot.us-east-2.amazonaws.com", 8883)
        self.client.configureCredentials("AmazonRootCA1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO 3: fill in the function to show your received message
        # print("client {} received payload {} from topic {}".format(self.device_id, , ))
        pass

    def default_message_handler(self, protocol, topic, message_id, status, route, message):
   
        # Process messages without a registered handler router target
        log.error('Received message to unknown route / message handler: {} - message: {}'.format(route, message))



    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass

    # pubsub_client = AwsGreengrassPubSubSdkClient("test1",default_message_handler)
    # pubsub_client.activate_mqtt_pubsub()
    def publish(self, topic="vehicle/data/broadcast"):
    # Load the vehicle's emission data
        
        # df = pd.read_csv(data_path.format(self.device_id))
        # for index,row in df.iterrows():
        #     # Create a JSON payload from the row data
        #     payload = json.dumps(row.to_dict())
        #     # sdk_format = formatter.get_message(message=payload)
        #     # pubsub_client.publish_message('mqtt',sdk_format,topic='vehicle/test')
        #     sdk_format = json.dumps(payload)
        #     # Publish the payload to the specified topic
        #     print(f"Publishing: {sdk_format} to {topic}")
        #     self.client.publish(topic, sdk_format, 0)

        df = pd.read_csv(data_path)
             
        # Publish each row as a JSON payload
        for _, row in df.iterrows():
            CO2_val = float(row['vehicle_CO2'])
            vehicle_stat = row['vehicle_id']
            print("CO2_val:", CO2_val)
            print("vehicle_stat:", vehicle_stat)
            
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            data = {
                    "CO2_val": CO2_val,
                    "vehicle_id": vehicle_stat,
                    "Time": formatted_time
                }
            payload = json.dumps(data)
            # vehicle_topic = f"mqtt/lab4sec2/{self.device_id}/{vehicle_stat}"

            print(f"Publishing: {payload} to {topic}")
            self.client.publish(topic, payload, 0)
            
            # Sleep to simulate real-time data publishing
            



print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for i in range(device_st, device_end):
    device_id = 'thing_'+str(i)
    certificate_formatter = device_id+"_cert.pem"
    key_formatter = device_id+"_private.key"
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    client.client.connect()
    clients.append(client)
 

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            c.publish()

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)
