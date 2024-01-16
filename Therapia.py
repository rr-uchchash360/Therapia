# ===================LIBRARY IMPORTS=======================

import os
import csv
import time
import sys  
import serial 
import numpy as num
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from serial.tools import list_ports
from pathlib import Path
from scipy.signal import butter, filtfilt
import Portal as gui 
#import ObjectResource as object
import CanvasGraph as graph  
from PyQt5.uic import loadUi 
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

class Main(gui.Ui_MainWindow, QtWidgets.QMainWindow):
    temp = []
    update_signal = QtCore.pyqtSignal(list)  # Signal for updating the GUI
    #==========INITIAL CLASS FUNCTION================ 
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.button_connectdisconnect_2.clicked.connect(self.connectDevice)
        self.hand_angle_line = None
        self.a1 = 1.0  # Length of the link
        self.d1 = 0.5  # Distance from the base to the start of the link
        # Additional variables for filtering and hysteresis
        self.filtered_y = 0  # Filtered y-axis value
        self.prev_sign = 0  # Previous sign of the filtered y-axis value
        self.movements_count = 0  # Counter for abduction-adduction movements
        self.sensitivity = 0.1  # Adjust sensitivity as needed
        self.hysteresis_threshold_up = 0.2  # Threshold for upward movement
        self.hysteresis_threshold_down = -0.2  # Threshold for downward movement
        self.in_motion = False  # Flag to track if the hand is currently in motion
        #self.pushButton_2.clicked.connect(self.connectDevice)
        #self.update_signal.connect(self.update_gui)
        
        # Filter parameters
        self.filter_order = 2
        self.cutoff_frequency = 2.0 / 25.0  # Adjust cutoff frequency as needed (normalized to half the sampling frequency)

        # Design the filter
        self.b, self.a = butter(self.filter_order, self.cutoff_frequency, btype='low', analog=False, output='ba')

        self.update_signal.connect(self.update_angle_display)
        # Connect the signal to the update_gui method
    # Initialize entry form and define its objects

        self.entry_form = QtWidgets.QMainWindow()  # initialize the information entry form
          # create an object of Entry_Form_PSAR (Post Stroke Arm Rehabilitation)
        
        self.entry_form.setWindowTitle('Patient Information Entry Form')  # set window title
    # *Define variables.*
        self.coordinatesinit = num.zeros((3, 8), dtype='float')  # define array to store initial co-ordinate values
    # Graph Setup
        self.gobj = graph.CanvasGraph(self.frame_3dGraph)  # create an object of type canvasgraph for main window
        self.color_ = '#236b9b'  # define line color
        self.fig = self.gobj.fig  # assign 3D fig
        self.ax = self.gobj.ax  # assign 3D axes
        self.setupgrid()  # draw axes
        self.line3d, = self.ax.plot(self.coordinatesinit[0], self.coordinatesinit[1], self.coordinatesinit[2], linewidth=4, marker='o', markersize=6, markeredgecolor='c', markerfacecolor='w',
                                    color=self.color_)  # define line
        self.gobj.move(16, 16)  # move canvas
    #==========Partesina Tai ekhane implement kora===========
        #a1=17.5
        self.prevvalue = 0.0
        self.transform_matrix_length = 7
        self.max = 0
        self.min = 0
        self.portFound = False 
        self.motion_param_length = 4  # define the length of list of motion
        self.angleslength = 10  # define the length of list of angles
        self.datalength = 6
            
            # arm yaw-pitch-roll
        self.armyaw = 0.0
        self.armyaw2 = 0.0
        self.armpitch = 0.0
        self.armpitch2 = 0.0
        self.armroll = 0.0
        self.armroll2 = 0.0
            
        #self.a1 = a1
        self.coordinates = num.zeros((3, 8), dtype='float')
    def setcoordinates(self, coordinates):

        if type(coordinates) == list:
            # iterate through the coordinates list
            for i in range(0, 3):
                self.coordinates[i] = coordinates[i]  # assign values

            self.resetgrid()  # reset grid
            self.line3d, = self.ax.plot(self.coordinates[0], self.coordinates[1], self.coordinates[2], linewidth=4, marker='o', markersize=6, markeredgecolor='c', markerfacecolor='w',
                                        color=self.color_)  # define line
            self.gobj.draw()  # draw object
            self.fig.canvas.flush_events()  # flush events
        else:
            self.resetgrid(b1=True)
    # ================================KINEMATICS BLOCK===================================================
    def calculateHandAngle(self, y):
        a1=1.0 #Length of the link
        d1=0.5 #Distance from the base to the start of the link
        y = num.radians(y)
        alpha = [0]
        a = [a1]
        d = [d1]
        
        T = num.array([
            [num.cos(y), -num.sin(y), 0, a[0]*num.cos(y)],
            [num.sin(y), num.cos(y), 0, a[0]*num.sin(y)],
            [0, 0, 1, d[0]],
            [0, 0, 0, 1]
        ])
        
        theta_y = num.arctan2(T[0, 2], T[2, 2])
        theta_y = num.degrees(theta_y)
        return theta_y
    #def updateHandAngle(self, y):
    # def update_angle_display(self, angles):
    #     #self.value_angularValue.setText(f'Hand Angles: {angles}')
    #     self.value_angularValue.setText(QApplication.translate("Form", "Angle:" + angles, None))

    #     # Check for a change in sign to detect abduction-adduction movement
    #     # if num.sign(current_angle_y) != num.sign(self.prev_angle_y):
    #     #     self.movements_count += 1
    #     #     self.label_movements.setText(f'Abduction-Adduction Movements: {self.movements_count}')
    #     # self.prev_angle_y = current_angle_y
    #     # if hasattr(self, 'hand_angle_line'):
    #     #     self.hand_angle_line.remove()  # Remove the previous line

    # # Calculate the coordinates for the hand angle line
    #     x = num.linspace(0, 0, 50)  # x-coordinate remains constant
    #     y = num.linspace(0, 0, 50)  # y-coordinate remains constant
    #     z = num.linspace(-25, 25, 50)  # z-coordinate corresponds to the hand angle

    #     # Plot the hand angle line
    #     self.hand_angle_line, = self.ax.plot(x, y, z, color='red', linewidth=4, label='Hand Angle')
        
    #     # Redraw the 3D graph
    #     self.fig.canvas.draw()
    def update_angle_display(self, angles):
        if not angles:
            return  # Return early if the input is empty

        y = angles[0]  # Extract the y-axis value from the list

        if not num.isscalar(y):
            return  # Return early if the y value is not a scalar (e.g., not a number)

        # Apply filtering
        #self.filtered_y = filtfilt(self.b, self.a, [y], padlen=50)  # Adjust padlen as needed

        self.value_angularValue.setText(QApplication.translate("Form", "Angle:" + str(y), None))

        # y = angles[0]  # Extract the y-axis value from the list
        # self.filtered_y = filtfilt(self.b, self.a, y)
        # self.value_angularValue.setText(QApplication.translate("Form", "Angle:" + str(y), None))

        # Calculate the coordinates for the hand angle line using Denavit-Hartenberg parameters
        theta_y = num.radians(y)
        T = num.array([
            [num.cos(theta_y), -num.sin(theta_y), 0, self.a1 * num.cos(theta_y)],
            [num.sin(theta_y), num.cos(theta_y), 0, self.a1 * num.sin(theta_y)],
            [0, 0, 1, self.d1],
            [0, 0, 0, 1]
        ])

        # Get the position from the transformation matrix
        hand_position = T[:3, 3]

        # Check if hand_angle_line is None, create the line
        if self.hand_angle_line is None:
            scaling_factor = 15  # Adjust the scaling factor as needed
            hand_line_x = [0, scaling_factor * hand_position[0]]
            hand_line_y = [0, scaling_factor * hand_position[1]]
            hand_line_z = [0, scaling_factor * hand_position[2]]
            self.hand_angle_line, = self.ax.plot(hand_line_x, hand_line_y, hand_line_z,
                                                color='black', linewidth=4, label='Hand Angle')  # Increase linewidth to 8 or your desired value
        else:
    # Update the data of the existing hand angle line
            scaling_factor = 15  # Adjust the scaling factor as needed
            self.hand_angle_line.set_xdata([0, scaling_factor * hand_position[0]])
            self.hand_angle_line.set_ydata([0, scaling_factor * hand_position[1]])
            self.hand_angle_line.set_3d_properties([0, scaling_factor * hand_position[2]])
            self.hand_angle_line.set_linewidth(4)  # Increase linewidth to 8 or your desired value

        # Motion count algorithm with sensitivity and hysteresis
        # current_sign = num.sign(self.filtered_y)

        # if not self.in_motion and abs(self.filtered_y) > self.sensitivity:
        #     # Hand is starting a new movement
        #     self.in_motion = True

        #     if current_sign == 1 and self.prev_sign == 0:
        #         # Hand is moving upward
        #         self.movements_count += 1
        #     elif current_sign == -1 and self.prev_sign == 0:
        #         # Hand is moving downward
        #         self.movements_count += 1

        #     # Update the label or perform any action to display the count
        #     self.value_motion.setText(str(self.movements_count))

        # elif self.in_motion and abs(self.filtered_y) < self.sensitivity:
        #     # Hand has returned to a rest position
        #     self.in_motion = False

        # self.prev_sign = current_sign  # Update the previous sign for the next iteration
        # # Redraw the 3D graph
        self.fig.canvas.draw()



    #==========CONNECT DEVICE EVENT================
    def connectDevice(self):
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
                    self.showSuccessfulConnectionStatus(port) 
                    self.button_connectdisconnect_2.setText('Disconnect')  
                    #print('Connected to ' + str(port.name))
                    self.label_connectionStatus.setText('Connected')
                    self.timer = QtCore.QTimer()
                    self.timer.timeout.connect(lambda: self.readAndDisplay(serialObj))
                    #self.resetgrid(b1=False) 
                    self.timer.start(5)  # Set the timer interval in milliseconds 
                return ret  # return the serial object
            else:  # handshake was not valid, move on to the next device in the list
                serialObj.close()  # close the current serial object

        if not flag_portFound:
            self.showFailedConnectionStatus() 
            self.button_connectdisconnect_2.setText('Connect') 
            #self.label_connectionStatus.setText('Disconnected')
            print('Could not find device! Check device connection!')
        return ret  # return value

    #==========READ AND DISPLAY EVENT================
    # def readAndDisplay(self, serialObj):
    #     temp = list(str(serialObj.readline().decode().split('\r\n')[0]).split(','))
    #     _data = [float(value) for value in temp]
    #     self.update_signal.emit(temp)  # Emit the signal with the new data
    def readAndDisplay(self, serialObj):
        temp = list(str(serialObj.readline().decode().split('\r\n')[0]).split(','))
        _data = [float(value) for value in temp]
        print(_data[1])
        self.update_signal.emit([_data[1]]) 
        # Emit the signal with the y-axis value in a list
  # Emit the signal with the y-axis value


    def update_gui(self, data):
        self.value_angularValue.setText(QApplication.translate("Form", "Angle:" + data[1], None))
    #     self.label_17.setText(QApplication.translate("Form", "Data 1 :" + data[0], None))
    #     self.label_19.setText(QApplication.translate("Form", "Data 2 :" + data[1], None))
    #     self.label_21.setText(QApplication.translate("Form", "Data 3 :" + data[2], None))
    #     self.label_24.setText(QApplication.translate("Form", "Data 4 :" + data[3], None))
    #     self.label_27.setText(QApplication.translate("Form", "Data 5 :" + data[4], None))
    #     self.label_28.setText(QApplication.translate("Form", "Data 6 :" + data[5], None))
    # def update_angle_display(self, data):
    #     angle = self.calculateHandAngle(float(data[1]))
    #     self.value_angularValue.setText(QApplication.translate("Form", str(angle), None))
    #==========CONNECT STATUS MESSAGE BOX================
    def showSuccessfulConnectionStatus(self, PORT):
        msg = QMessageBox()
        msg.setWindowTitle("Connection Status")
        #msg.setText("Connection Successful")
        msg.setText('Connected to ' + str(PORT.name))
        x=msg.exec_()
    def showFailedConnectionStatus(self):
        msg = QMessageBox()
        msg.setWindowTitle("Connection Status")
        msg.setText("No Device Found!")  
        x=msg.exec_()  
    def setupgrid(self):
        self.ax.axis('off')  # switch axes off

        # draw the x-axis
        x = num.linspace(-25, 25, 50)  # define values
        y = num.linspace(0, 0, 50)  # define values
        z = num.linspace(0, 0, 50)  # define values
        self.ax.plot(x, y, z, color='#b0041b', linewidth=1.5, label='X-Axis')  # plot the values

        # draw the y-axis
        x = num.linspace(0, 0, 50)  # define values
        y = num.linspace(-25, 25, 50)  # define values
        z = num.linspace(0, 0, 50)  # define values
        self.ax.plot(x, y, z, color='g', linewidth=1.5, label='Y-Axis')  # plot the values

        # draw the z-axis
        x = num.linspace(0, 0, 50)  # define values
        y = num.linspace(0, 0, 50)  # define values
        z = num.linspace(-25, 25, 50)  # define values
        self.ax.plot(x, y, z, color=self.color_, linewidth=1.5, label='Z-Axis')
    
    
        def resetgrid(self, b1=False):
            plt.cla()  # clear axes
            self.setupgrid()  # setup the grid

            # Remove the previous hand angle line if it exists
            if hasattr(self, 'hand_angle_line'):
                self.hand_angle_line.remove()

            # Check if value is true
            if b1:
                self.line3d, = self.ax.plot(self.coordinatesinit[0], self.coordinatesinit[1], self.coordinatesinit[2],
                                            linewidth=4, marker='o', markersize=6, markeredgecolor='c', markerfacecolor='w',
                                            color=self.color_)  # define line
                self.gobj.draw()  # draw object
                self.fig.canvas.flush_events()  # flush events

# # ===================MAIN FUNCTION=======================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
