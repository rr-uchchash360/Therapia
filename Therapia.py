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
import Portal as gui 
#import ObjectResource as object
import CanvasGraph as graph  
from PyQt5.uic import loadUi 
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Entry_Form_PSAR import Ui_MainWindow_Info

class Main(gui.Ui_MainWindow, QtWidgets.QMainWindow):
    temp = []
    update_signal = QtCore.pyqtSignal(list)  # Signal for updating the GUI
    
    #==========INITIAL CLASS FUNCTION================ 
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.button_connectdisconnect_2.clicked.connect(self.connectDevice)
        #self.pushButton_2.clicked.connect(self.connectDevice)
        self.update_signal.connect(self.update_gui)  # Connect the signal to the update_gui method
    # Initialize entry form and define its objects
        self.entry_form = QtWidgets.QMainWindow()  # initialize the information entry form
        self.form_object = Ui_MainWindow_Info()  # create an object of Entry_Form_PSAR (Post Stroke Arm Rehabilitation)
        self.form_object.setupUi(self.entry_form)  # setup UI
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
                    self.button_connectdisconnect_2('Disconnect')  
                    #print('Connected to ' + str(port.name))
                    self.label_connectionStatus.setText('Connected to ' + str(port.name))
                    self.timer = QtCore.QTimer()
                    self.timer.timeout.connect(lambda: self.readAndDisplay(serialObj))
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
    def readAndDisplay(self, serialObj):
        temp = list(str(serialObj.readline().decode().split('\r\n')[0]).split(','))
        self.update_signal.emit(temp)  # Emit the signal with the new data

    def update_gui(self, data):
        self.label_17.setText(QApplication.translate("Form", "Data 1 :" + data[0], None))
        self.label_19.setText(QApplication.translate("Form", "Data 2 :" + data[1], None))
        self.label_21.setText(QApplication.translate("Form", "Data 3 :" + data[2], None))
        self.label_24.setText(QApplication.translate("Form", "Data 4 :" + data[3], None))
        self.label_27.setText(QApplication.translate("Form", "Data 5 :" + data[4], None))
        self.label_28.setText(QApplication.translate("Form", "Data 6 :" + data[5], None))
        
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
        
# # ===================MAIN FUNCTION=======================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
# # ===================APPLICATION CLASS=======================
# # Defining the class
# class Application(gui.TherapyPortal, QtWidgets.QMainWindow):
#     # ===================CLASS INITIALIZATION=======================
#     def __init__(self):
#         super(Application, self).__init__() # initialize
#         self.setupUi(self) # set window
#         self.setWindowTitle("Therapia") # set window title
#     # ===================DEFINING THREADS=======================
#         self.thread_portConnect = WorkerThread(self, 'portConnect')
#         self.threadcontrol() #connect threads to class functions
                
#     # ===================DEFINING THREADS=======================
#     def threadcontrol(self):
#         self.thread_portConnect.signalbool.connect(self.portConnect) #connect signal from checkport thread
    
#     # ===================DEVICE CONNECTION=======================
#     def connectDevice(self):
#         self.serial, self.flag_portFound = system.portConnect() #connect to device  
#         #check if port is found
#         if self.flag_portFound:
#             self.thread_portConnect.start()
#             self.pushButton_ConnectWithHardware.setText('Disconnect')
#             self.setmsg(['Serial Connection', QtWidgets.QMessageBox.Information, 'Serial connection successful at {}'.format(str(self.serial.name))])  # set message
#         else:  # handshake was not valid, move on to the next device in the list
#             self.flag_connectdisconnect = False  # assign values
#             self.button_connectdisconnect.setChecked(False)  # assign values
#             self.setmsg(['Serial Connection', QtWidgets.QMessageBox.Warning, 'Serial connection failed! Could not find COM port'])  # set message
          
# # ===================WORKERTHREAD CLASS=======================
# class WorkerThread(QThread):
#     signalbool = pyqtSignal(bool)
#     def __init__(self, parent=None, function=None):
#         QThread.__init__(self, parent)
#         self.function = function
#     def run(self):
#         if self.function == 'portConnect':
#             self.signalbool.emit(True)
#     def stop(self):
#         self.terminate()
        
# # ===================MAIN FUNCTION=======================


# app = QtWidgets.QApplication(sys.argv)  # if PyQt5 is used
# qt_app = Application()  # create an object of class Application (Post Stroke Arm Rehabilitation)
# qt_app.show()  # display the interface
# sys.exit(app.exec_())  # execute the app