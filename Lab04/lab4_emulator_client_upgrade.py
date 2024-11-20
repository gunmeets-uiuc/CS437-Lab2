from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd


# MQTT Client Base Class
class MQTTClient:
    def __init__(self, device_id, cert, key, endpoint, root_ca):
        self.device_id = str(device_id)
        self.client = AWSIoTMQTTClient(self.device_id)
        
        # Configure endpoint and certificates
        self.client.configureEndpoint(endpoint, 8883)
        self.client.configureCredentials(root_ca, key, cert)
        
        # Configure connection properties
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
        self.client.configureDrainingFrequency(2)        # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10) # 10 sec
        self.client.configureMQTTOperationTimeout(5)      # 5 sec
        
        # Custom onMessage handler for subscribers
#        self.client.onMessage = self.customOnMessage

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()

    def customOnMessage(self, client, userdata, message):
        print(f"Message received on {message.topic}: {message.payload.decode()}")


# Publisher Class
class Publisher(MQTTClient):
    def __init__(self, device_id, cert, key, endpoint, root_ca, data_path):
        super().__init__(device_id, cert, key, endpoint, root_ca)
        self.data_path = data_path

    def publish_data(self, topic="vehicle/emission/data"):

        print("Topic:", topic)
        # Load data from CSV
        df = pd.read_csv(self.data_path)
        
        # Publish each row as a JSON payload
        for _, row in df.iterrows():
            payload = json.dumps(row.to_dict())
            print("************************************************ - Purlisher - *************************************************")		
            print(f"[Publisher {self.device_id}] Publishing to {topic}: {payload}")
            self.client.publish(topic, payload, 1)
            time.sleep(2)  # Delay for real-time emulation


# Subscriber Class
class Subscriber(MQTTClient):
    def __init__(self, device_id, cert, key, endpoint, root_ca, topic):
        super().__init__(device_id, cert, key, endpoint, root_ca)
        self.topic = topic
        self.client.subscribe(self.topic, 1, self.customOnMessage)

    def customOnMessage(self, client, userdata, message):
    # Access message topic and payload
        topic = message.topic

        Device1, Device2 = self.device_id.split("|")
        payload = message.payload.decode("utf-8")  # Decode the payload if it's in bytes
        print("################################# - Subscriber - ###############################")
        print("********* - ", Device1)
        print(f"Client {Device1} received payload {payload} from topic {topic}")
        print("********* - ", Device2)
        print(f"Client {Device2} received payload {payload} from topic {topic}")


# Configuration Parameters
device_start = 0
device_end = 3
endpoint = "a2mldvnrhxco3b-ats.iot.us-east-1.amazonaws.com"
root_ca = "/Users/biplab/desktop/Biplab/MS/CS437/lab04/Lab04AmazonRootCA1.pem"
certificate_formatter = "/Users/biplab/desktop/Biplab/MS/CS437/lab04/IotThing{}_cert.pem"
key_formatter = "/Users/biplab/desktop/Biplab/MS/CS437/lab04/IotThing{}_private.key"
data_path_formatter = "/Users/biplab/desktop/Biplab/MS/CS437/lab04/vehicle{}.csv"
topic = "vehicle/emission/data"


# Initialize Publishers and Subscribers
publishers = []
subscribers = []

for device_id in range(device_start, device_end):
    cert = certificate_formatter.format(device_id)
    key = key_formatter.format(device_id)
    data_path = data_path_formatter.format(device_id)

    # Initialize Publisher
    publisher = Publisher(f"IotThing{device_id}", cert, key, endpoint, root_ca, data_path)
    publisher.connect()
    publishers.append(publisher)

    # Initialize Subscriber
    subscriber = Subscriber("IotThing3|IotThing4", cert, key, endpoint, root_ca, topic)
    subscriber.connect()
    subscribers.append(subscriber)


# Main Execution Loop
try:
    while True:
        print("Press 's' to start publishing, 'd' to disconnect all devices, or 'q' to quit.")
        command = input("Enter command: ")
        
        if command == "s":
            for pub in publishers:
                pub.publish_data(topic)

        elif command == "d":
            for pub in publishers:
                pub.disconnect()
            for sub in subscribers:
                sub.disconnect()
            print("All devices disconnected")

        elif command == "q":
            for pub in publishers:
                pub.disconnect()
            for sub in subscribers:
                sub.disconnect()
            print("Exiting program.")
            break
        else:
            print("Invalid command.")

        time.sleep(3)

except KeyboardInterrupt:
    print("Program interrupted. Disconnecting all devices.")
    for pub in publishers:
        pub.disconnect()
    for sub in subscribers:
        sub.disconnect()
