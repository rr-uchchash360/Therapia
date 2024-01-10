# ================================ Responsible for connection with HW =======================================



import threading as th
import numpy as np
import serial
import time
import csv
import os

from serial.tools import list_ports
from pathlib import Path

flag_continue = True

def continue_():
    global flag_continue

    input()
    flag_continue = False


def portConnect():
    portList = list(serial.tools.list_ports.comports())  # get list of available serial ports
    flag_portFound = False  # set the port found flag
    ret = [None, flag_portFound]

    for port in portList:  # find the active port
        print('Checking port ' + str(port.name))
        serialObj = serial.Serial(str(port.device), baudrate=19200, timeout=2.0)  # setup serial connection
        handShakeVal = serialObj.readline().decode('ascii')  # retrieve the handshake value sent by SRS

        if handShakeVal == str('a' + '\r\n'):  # check if handshake is valid
            serialObj.write(b'a')  # as handshake was valid write back the handshake value to start data retrieval
            flag_portFound = True  # set the port found flag
            ret = [serialObj, flag_portFound]  # define list to store port and status
            if flag_portFound:
                print('Connected to ' + str(port.name))

            return ret  # return the serial object
        else:  # handshake was not valid, move on to the next device in the list
            serialObj.close()  # close the current serial object

    if not flag_portFound:
        print('Could not find device! Check device connection!')

    return ret  # return value


def portDisconnect(serialObj):
    serialObj.write(b'e')  # as handshake was valid write back the handshake value to start data retrieval
    serialObj.close()  # close the serial port
    print('Disconnected from ' + str(serialObj.name))

    ret = [None, False]
    return ret  # return the flag


def fetchData(serialObj, flag_isConnected):
    try:
        if flag_isConnected:
            temp = list(str(serialObj.readline().decode().split('\r\n')[0]).split(','))  # retrieve individual data as 'string'
            _data = [float(value) for value in temp]

            if type(_data) is not None:
                return _data

    except serial.SerialException as SE:
        # portDisconnect(serialObj)
        print(serialObj, "Device unplugged unexpectedly!")


port, flag_isConnected = portConnect()

th.Thread(target=continue_, args=(), name='continue_', daemon=True).start()
while flag_continue:
    data = fetchData(port, flag_isConnected)
    print(data)
    time.sleep(.001)

if flag_isConnected:
    port, flag_isConnected = portDisconnect(port)
