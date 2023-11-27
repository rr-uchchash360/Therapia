# ===================LIBRARY IMPORTS=======================

import os
import csv
import time
import System as system
import numpy as np
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from serial.tools import list_ports
from pathlib import Path
import TherapyPortal as gui 
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets, QtGui, QtCore
from pathlib import Path
# ===================APPLICATION CLASS=======================
# Defining the class
class Application(gui.TherapyPortal, QtWidgets.QMainWindow):
    # ===================CLASS INITIALIZATION=======================
    def __init__(self):
        super(Application, self).__init__() # initialize
        self.TherapyPortalUi(self) # set window
        self.setWindowTitle("Therapia") # set window title
    # ===================DEFINING THREADS=======================
        self.thread_portConnect = WorkerThread(self, 'portConnect')
        self.threadcontrol() #set up threads
        
    # ===================DEFINING THREADS=======================
    def threadcontrol(self):
        self.thread_portConnect.signalbool.connect(self.portConnect) #connect signal from checkport thread
    # ===================DEVICE CONNECTION=======================
    def connectDevice(self):
        self.serial, self.flag_portFound = system.portConnect() #connect to device  
        #check if port is found
        if self.flag_portFound:
            self.thread_portConnect.start()
            self.pushButton_ConnectWithHardware.setText('Disconnect')
            self.setmsg(['Serial Connection', QtWidgets.QMessageBox.Information, 'Serial connection successful at {}'.format(str(self.serial.name))])  # set message
        else:  # handshake was not valid, move on to the next device in the list
            self.flag_connectdisconnect = False  # assign values
            self.button_connectdisconnect.setChecked(False)  # assign values
            self.setmsg(['Serial Connection', QtWidgets.QMessageBox.Warning, 'Serial connection failed! Could not find COM port'])  # set message
          
# ===================WORKERTHREAD CLASS=======================
class WorkerThread(QThread):
    signalbool = pyqtSignal(bool)
    def __init__(self, parent=None, function=None):
        QThread.__init__(self, parent)
        self.function = function
    def run(self):
        if self.function == 'portConnect':
            self.signalbool.emit(True)
    def stop(self):
        self.terminate()
        
# ===================MAIN FUNCTION=======================
def main():
    app = QtWidgets.QApplication(sys.argv) #create application
    application = Application() #create application
    application.show() #show application
    sys.exit(app.exec_()) #execute application