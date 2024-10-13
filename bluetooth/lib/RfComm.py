## This code will run on the raspberry pi system ##

import picar_4wd as fc
import sys
from bluedot.btcomm import BluetoothServer
from signal import pause

def data_received(data):
    print(data)
    if data == 'power level':
        send_data = str(fc.power_read())
    s.send(send_data)

s = BluetoothServer(data_received)
pause()