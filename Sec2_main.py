import sys
import time
import traceback
import json

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
import awsiot.greengrasscoreipc.clientv2 as clientV2
from awsiot.greengrasscoreipc.model import (
    SubscriptionResponseMessage,
    UnauthorizedError
)
from awsiot.greengrasscoreipc.model import (
    PublishMessage,
    BinaryMessage)

global ipc_client
ipc_client = GreengrassCoreIPCClientV2()
global maxCounterLst
maxCounterLst = {}
maxCounterLst["veh0"] = 0.0
maxCounterLst["veh1"] = 0.0
maxCounterLst["veh2"] = 0.0

def main():
    topic = 'vehicle/data/broadcast'
    global ipc_client

    try:
        
        # Subscription operations return a tuple with the response and the operation.
        # _, operation = ipc_client.subscribe_to_topic(topic=topic, on_stream_event=on_stream_event,
        #                                              on_stream_error=on_stream_error, on_stream_closed=on_stream_closed)
        resp, operation = ipc_client.subscribe_to_iot_core(
        topic_name=topic,
        qos=1, 
        on_stream_event=on_stream_event,
        on_stream_error=on_stream_error,
        on_stream_closed=on_stream_closed
        )
        print('Successfully subscribed to topic: ' + topic)
        print('Respose: ' , resp)
        print('operaton:' , operation)
        # if message:
        #     msg = message
        # else:
        #     msg = 'TEST'
        # msg = 'TEST'
        

        # Keep the main thread alive, or the process will exit.
        try:
            while True:

                # publish_binary_message_to_topic(ipc_client)
                # topic = 'my/topic'
                # qos = '1'
                # payload = 'Hello, World'
                # ipc_client = clientV2.GreengrassCoreIPCClientV2()
                # resp = ipc_client.publish_to_iot_core(topic_name=topic, qos=qos, payload=payload)
                # ipc_client.close()
                time.sleep(10)
        except InterruptedError:
            print('Subscribe interrupted.')

        # To stop subscribing, close the stream.
        operation.close()
    except UnauthorizedError:
        print('Unauthorized error while subscribing to topic: ' +
              topic, file=sys.stderr)
        traceback.print_exc()
        exit(1)
    except Exception:
        print('Exception occurred', file=sys.stderr)
        traceback.print_exc()
        exit(1)

def publish_message_to_topic(ipc_client,timestep,vehicle_id,co2_emission,topic_out):
    
    print('sending message to respective vehicle')
    global maxCounterLst
    print("dict:" , maxCounterLst[vehicle_id], co2_emission)

    if co2_emission > maxCounterLst[vehicle_id]:
        maxCounterLst[vehicle_id] = float(co2_emission)
    data_out = {
                "Maxvehicle_CO2": maxCounterLst[vehicle_id],
                "vehicle_id": vehicle_id,
                "Time": timestep
            }
    payload_out = json.dumps(data_out)
    resp = ipc_client.publish_to_iot_core(topic_name=topic_out, qos=1, payload=payload_out)
    # ipc_client.close()
    return ipc_client.publish_to_topic(topic=topic_out, publish_message=payload_out)


def on_stream_event(event: SubscriptionResponseMessage) -> None:
    global ipc_client
    try:
        
        message = event.message
        topic_name = event.message.topic_name
        print(f'Received new message on topic {topic_name}:  {message}')
        
        # Decode the payload 
        payload_bytes = message.payload  # Payload is usually in bytes 
        payload_str = payload_bytes.decode('utf-8')        # Convert bytes to string print(f"Raw Payload: {payload_str}"
        data = json.loads(payload_str) 
        # print(f"Decoded Message: {data}") # Extract specific fields
        timestep = data.get("Time", None) 
        vehicle_id = data.get("vehicle_id", None) 
        co2_emission = data.get("CO2_val")
        # print("co2_emission:" , co2_emission)
        # print("vehicle_id:" , vehicle_id)
        # print("timestep:" , timestep)
        
        
        topic_out = vehicle_id + '/data/out'
        publish_message_to_topic(ipc_client,timestep,vehicle_id,co2_emission,topic_out)
    except:
        traceback.print_exc()


def on_stream_error(error: Exception) -> bool:
    print('Received a stream error.', file=sys.stderr)
    traceback.print_exc()
    return False  # Return True to close stream, False to keep stream open.


def on_stream_closed() -> None:
    print('Subscribe to topic stream closed.')


if __name__ == '__main__':
    main()
