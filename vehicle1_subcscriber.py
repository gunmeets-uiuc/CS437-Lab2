from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging


class Subscriber:
    def __init__(self, device_id, cert, key, endpoint, root_ca, topic):
        self.device_id = device_id
        self.topic = topic
        self.client = AWSIoTMQTTClient(self.device_id)


        # Configure endpoint and credentials
        self.client.configureEndpoint(endpoint, 8883)
        self.client.configureCredentials(root_ca, key, cert)


        # Configure client settings
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
        self.client.configureDrainingFrequency(2)        # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10) # 10 sec
        self.client.configureMQTTOperationTimeout(5)      # 5 sec


        # Enable logging for debugging
        # logging.basicConfig(level=logging.DEBUG)
        # logger = logging.getLogger("AWSIoTPythonSDK.core")


    def connect(self):
        print(f"[{self.device_id}] Connecting to AWS IoT...")
        self.client.connect()
        print(f"[{self.device_id}] Connected.")


    def subscribe(self):
        print(f"[{self.device_id}] Subscribing to {self.topic}...")
        self.client.subscribe(self.topic, 1, self.customOnMessage)
        print(f"[{self.device_id}] Subscribed to {self.topic}.")


    def customOnMessage(self, client, userdata, message):
        # Decode and print the received message
        payload = message.payload.decode("utf-8")
        print(f"[{self.device_id}] Received message from {message.topic}: {payload}")


    def disconnect(self):
        self.client.disconnect()
        print(f"[{self.device_id}] Disconnected.")


 



      
endpoint = "avsk2qeejl1gz-ats.iot.us-east-2.amazonaws.com"
root_ca = "AmazonRootCA1.pem"
cert = "thing_11_cert.pem"
key = "thing_11_private.key"
topic = "veh1/data/out"


subscriber = Subscriber("SubscriberDevice1", cert, key, endpoint, root_ca, topic)


try:
    subscriber.connect()
    subscriber.subscribe()
    print("Listening for messages... (Press Ctrl+C to exit)")
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    subscriber.disconnect()