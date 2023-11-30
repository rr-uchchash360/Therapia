from PyQt5.QtWidgets import QApplication, QMainWindow
from AddPatient import Ui_MainWindow # Replace with your actual file name
import sys  # Add this line to import the sys module

import sys
import os
import json
import re
import datetime


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Call the setupUi method from AddPatient
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())