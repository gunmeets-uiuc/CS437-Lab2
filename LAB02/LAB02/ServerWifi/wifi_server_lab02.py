from datetime import datetime
from websocket_server import WebsocketServer
import json
import time
import picar_4wd as fc
import sys
import tty
import termios
import asyncio

# Placeholder for car speed and distance
car_speed = 0
distance_traveled = 0
cpu_temp = 0
cpu_usage = 0
gpu_temp = 0
batt = 0
DiskU = ' '
RAMu = ' '

global Current_Instruction
global Previous_Instruction
Current_Instruction = ' '
Previous_Instruction = ' '

global Current_Time
global Previous_Time
Current_Time=' '
Previous_Time=' '

def get_parameters():
    parameters = fc.pi_read()
    print("Power:parameter", parameters)
    # Logic to get the Raspberry Pi's temperature
    global cpu_temp 
    global cpu_usage
    global gpu_temp
    global batt 
    global DiskU 
    global RAMu 

    cpu_temp = parameters['cpu_temperature']
    gpu_temp = parameters['gpu_temperature']
    cpu_usage = float(parameters['cpu_usage'])  # Convert CPU usage to float if needed
    disk_total = parameters['disk'][0]         # Total disk space
    disk_used = parameters['disk'][1]          # Used disk space
    disk_free = parameters['disk'][2]          # Free disk space
    disk_usage_percentage = parameters['disk'][3]  # Disk usage percentage

    DiskU='Total disk space - '+disk_total+', Used disk space - '+disk_used+', Free disk space - '+disk_free+', Disk usage percentage - '+disk_usage_percentage 
    ram_total = str(parameters['ram'][0])           # Total RAM
    ram_used = str(parameters['ram'][1])            # Used RAM
    ram_free = str(parameters['ram'][2])            # Free RAM

    RAMu='Total RAM - '+ram_total+'MB, Used RAM - '+ram_used+'MB, Free RAM - '+ram_free+'MB'
    batt = parameters['battery']      # Battery level

   # return 25.0  # Placeholder value

def move_picar(direction):
    global car_speed
    global Current_Instruction
    global Previous_Instruction
    global Current_Time
    global Previous_Time

    if Current_Instruction == ' ':
       Previous_Instruction=direction
       Previous_Time=datetime.now()
#       Current_Instruction=direction
    else:
       Previous_Instruction = Current_Instruction
       Previous_Time=Current_Time
       
    Current_Instruction = direction
    Current_Time=datetime.now()

    if direction == "FORWARD":
        fc.forward(20) 
        print("Foward Command given..")
        car_speed = 20  # Example speed for forward movement
        # Add code to move the car forward
    elif direction == "BACKWARD":
        print("Backward Command given..")
        fc.backward(10)	
        car_speed = 10  # Example speed for backward movement
        # Add code to move the car backward
    elif direction == "LEFT":
        print("Left Turn Command given..")
        fc.turn_left(5)
        car_speed = 5  # You can set this to 0 or a turning speed
        # Add code to turn the car left
    elif direction == "RIGHT":
        print("Right Turn Command given..")
        fc.turn_right(5)	
        car_speed = 5  # You can set this to 0 or a turning speed
        # Add code to turn the car right
    elif direction == "STOP":
        print("Stop Command given..")
        fc.stop()
        car_speed = 0  # Stop the car
        

def handle_message(client, server, message):
    global distance_traveled
    global Previous_Time
    global Current_Time
    command = message.strip()
    move_picar(command)
    get_parameters()
    print("Currenr_Instruction:", Current_Instruction)
    print("Previous_Instruction:", Previous_Instruction)
    if Previous_Instruction=='RIGHT' or Previous_Instruction=='STOP' or Previous_Instruction=='LEFT':
       distance_traveled = distance_traveled + 0
    else:
       print("Current_Time:", Current_Time)
       print("Previous_Time:", Previous_Time)
       timeDiffSec=(Current_Time-Previous_Time).seconds
       print("timeDiffSec:", timeDiffSec)
       distance_traveled = distance_traveled + (34*timeDiffSec) #speed 20 - 42cm/second

  
 
    # Prepare response
    response = {
        "cputemperature": cpu_temp,
        "cpuusage": cpu_usage,
        "gputemperature": gpu_temp,
        "battery": batt,
        "Disk": DiskU,
        "RAM": RAMu, 
        "speed": car_speed,
        "distance": distance_traveled
    }
    server.send_message(client, json.dumps(response))

server = WebsocketServer(host='0.0.0.0', port=65432)
server.set_fn_message_received(handle_message)

print("Server listening on port 65432")
Current_Instruction=' '
Previous_Instruction=' '
server.run_forever()
