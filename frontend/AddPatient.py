# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddPatient.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import os
import json
import re
import datetime


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(311, 344)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_PatientName = QLabel(self.centralwidget)
        self.label_PatientName.setObjectName(u"label_PatientName")
        self.label_PatientName.setGeometry(QRect(10, 10, 91, 16))
        self.textEdit_PatientName = QLineEdit(self.centralwidget)
        self.textEdit_PatientName.setObjectName(u"textEdit_PatientName")
        self.textEdit_PatientName.setGeometry(QRect(100, 10, 201, 21))
        self.textEdit_PatientName.setTabletTracking(False)
        self.textEdit_Age = QLineEdit(self.centralwidget)
        self.textEdit_Age.setObjectName(u"textEdit_Age")
        self.textEdit_Age.setGeometry(QRect(100, 40, 201, 21))
        self.label_Age = QLabel(self.centralwidget)
        self.label_Age.setObjectName(u"label_Age")
        self.label_Age.setGeometry(QRect(10, 40, 91, 16))
        self.label_Gender = QLabel(self.centralwidget)
        self.label_Gender.setObjectName(u"label_Gender")
        self.label_Gender.setGeometry(QRect(10, 70, 91, 16))
        self.textEdit_ContactNumber = QTextEdit(self.centralwidget)
        self.textEdit_ContactNumber.setObjectName(u"textEdit_ContactNumber")
        self.textEdit_ContactNumber.setEnabled(True)
        self.textEdit_ContactNumber.setGeometry(QRect(100, 100, 201, 21))
        self.textEdit_ContactNumber.setMouseTracking(True)
        self.textEdit_ContactNumber.setAcceptDrops(True)
        self.textEdit_ContactNumber.setAutoFillBackground(False)
        self.textEdit_ContactNumber.setAcceptRichText(True)
        self.label_ContactNumber = QLabel(self.centralwidget)
        self.label_ContactNumber.setObjectName(u"label_ContactNumber")
        self.label_ContactNumber.setGeometry(QRect(10, 100, 91, 16))
        self.textEdit_Email = QLineEdit(self.centralwidget)
        self.textEdit_Email.setObjectName(u"textEdit_Email")
        self.textEdit_Email.setGeometry(QRect(100, 130, 201, 21))
        self.label_Email = QLabel(self.centralwidget)
        self.label_Email.setObjectName(u"label_Email")
        self.label_Email.setGeometry(QRect(10, 130, 91, 16))
        self.label_BloodGroup = QLabel(self.centralwidget)
        self.label_BloodGroup.setObjectName(u"label_BloodGroup")
        self.label_BloodGroup.setGeometry(QRect(10, 160, 91, 16))
        self.textEdit_TreatmentPlan = QTextEdit(self.centralwidget)
        self.textEdit_TreatmentPlan.setObjectName(u"textEdit_TreatmentPlan")
        self.textEdit_TreatmentPlan.setGeometry(QRect(100, 190, 201, 101))
        self.label_TreatmentPlan = QLabel(self.centralwidget)
        self.label_TreatmentPlan.setObjectName(u"label_TreatmentPlan")
        self.label_TreatmentPlan.setGeometry(QRect(10, 190, 91, 16))
        self.comboBox_Gender = QComboBox(self.centralwidget)
        self.comboBox_Gender.addItem("")
        self.comboBox_Gender.addItem("")
        self.comboBox_Gender.setObjectName(u"comboBox_Gender")
        self.comboBox_Gender.setGeometry(QRect(100, 70, 201, 22))
        self.comboBox_BloodGroup = QComboBox(self.centralwidget)
        self.comboBox_BloodGroup.addItem("")
        self.comboBox_BloodGroup.addItem("")
        self.comboBox_BloodGroup.addItem("")
        self.comboBox_BloodGroup.addItem("")
        self.comboBox_BloodGroup.addItem("")
        self.comboBox_BloodGroup.addItem("")
        self.comboBox_BloodGroup.addItem("")
        self.comboBox_BloodGroup.addItem("")
        self.comboBox_BloodGroup.setObjectName(u"comboBox_BloodGroup")
        self.comboBox_BloodGroup.setGeometry(QRect(100, 160, 201, 22))
        self.pushButton_AddPatient = QPushButton(self.centralwidget)
        self.pushButton_AddPatient.setObjectName(u"pushButton_AddPatient")
        self.pushButton_AddPatient.setGeometry(QRect(10, 300, 291, 23))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        
        
        
        # My cd
        self.textEdit_Age.setInputMask("999")
        
        
        
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Add Patient", None))
        self.label_PatientName.setText(QCoreApplication.translate("MainWindow", u"Patient's Name :", None))
        self.label_Age.setText(QCoreApplication.translate("MainWindow", u"Age :", None))
        self.label_Gender.setText(QCoreApplication.translate("MainWindow", u"Gender :", None))
        self.label_ContactNumber.setText(QCoreApplication.translate("MainWindow", u"Contact Number :", None))
        self.label_Email.setText(QCoreApplication.translate("MainWindow", u"Email :", None))
        self.label_BloodGroup.setText(QCoreApplication.translate("MainWindow", u"Blood Group :", None))
        self.label_TreatmentPlan.setText(QCoreApplication.translate("MainWindow", u"Treatment Plan :", None))
        self.comboBox_Gender.setItemText(0, QCoreApplication.translate("MainWindow", u"Male", None))
        self.comboBox_Gender.setItemText(1, QCoreApplication.translate("MainWindow", u"Female", None))

        self.comboBox_BloodGroup.setItemText(0, QCoreApplication.translate("MainWindow", u"A+", None))
        self.comboBox_BloodGroup.setItemText(1, QCoreApplication.translate("MainWindow", u"A-", None))
        self.comboBox_BloodGroup.setItemText(2, QCoreApplication.translate("MainWindow", u"B+", None))
        self.comboBox_BloodGroup.setItemText(3, QCoreApplication.translate("MainWindow", u"B-", None))
        self.comboBox_BloodGroup.setItemText(4, QCoreApplication.translate("MainWindow", u"AB+", None))
        self.comboBox_BloodGroup.setItemText(5, QCoreApplication.translate("MainWindow", u"AB-", None))
        self.comboBox_BloodGroup.setItemText(6, QCoreApplication.translate("MainWindow", u"O+", None))
        self.comboBox_BloodGroup.setItemText(7, QCoreApplication.translate("MainWindow", u"O-", None))

        self.pushButton_AddPatient.setText(QCoreApplication.translate("MainWindow", u"Add Patient", None))
    
    # retranslateUi
    
    def generate_patient_id(self):
        if self.validate_fields():
            now = datetime.datetime.now()
            year = now.year % 100
            month = now.month
            day = now.day

            gender = {"Male": 2, "Female": 1, "Other": 0}.get(self.comboBox_Gender.currentText(), 0)
            blood_group = {
                "O+": "01",
                "O-": "02",
                "A+": "11",
                "A-": "12",
                "B+": "21",
                "B-": "22",
                "AB+": "31",
                "AB-": "32",
            }.get(self.comboBox_Gender.currentText(), "00")

            phone_number = self.textEdit_ContactNumber.text()[-4:]
            patient_id = f"{year:02d}{month:02d}{day:02d}-{gender}-{blood_group}-{phone_number}"

            patient_data = {
                "Patient's Name": self.textEdit_PatientName.text(),
                "Age": self.textEdit_Age.text(),
                "Gender": self.comboBox_Gender.currentText(),
                "Contact Number": self.textEdit_ContactNumber.text(),
                "Email": self.textEdit_Email.text(),
                "Blood Group": self.comboBox_BloodGroup.currentText(),
                "Treatment Plan": self.textEdit_TreatmentPlan.toPlainText(),
            }

            default_directory = "patient_data"

            choice_msg = "Do you want to save the patient's data in the default location or choose another location?"
            choice_box = QMessageBox()
            choice_box.setIcon(QMessageBox.Question)
            choice_box.setText(choice_msg)
            choice_box.addButton(QPushButton("Default Location"), QMessageBox.YesRole)
            choice_box.addButton(QPushButton("Another Location"), QMessageBox.NoRole)
            user_choice = choice_box.exec_()

            if user_choice == 0:
                directory = os.path.join(os.getcwd(), default_directory)
            else:
                directory = QFileDialog.getExistingDirectory(None, "Select Directory", default_directory)

            if directory:
                folder_path = os.path.join(directory, patient_id)

                if os.path.exists(folder_path):
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Question)
                    msg_box.setText("A folder with the same Patient ID already exists. Do you want to overwrite it?")
                    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    msg_box.setDefaultButton(QMessageBox.No)
                    user_choice = msg_box.exec_()

                    if user_choice == QMessageBox.No:
                        return

                os.makedirs(folder_path, exist_ok=True)

                json_file_path = os.path.join(folder_path, f"{patient_id}.json")
                with open(json_file_path, "w") as json_file:
                    json.dump(patient_data, json_file, indent=4)

                message = f"Patient has been created successfully. Patient ID: <span style='color: blue;'>{patient_id}</span>"
                msg_box = QMessageBox()
                msg_box.setTextFormat(Qt.RichText)
                msg_box.information(None, "Patient ID", message)
            else:
                msg_box = QMessageBox()
                msg_box.setText("No directory selected. Please select a directory to save the patient's data.")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Please correct the following errors:\n\n" + self.get_error_messages())
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.exec_()
    
    def validate_fields(self):
        self.error_messages = []

        if not self.textEdit_PatientName.text():
            self.error_messages.append("Patient's Name is empty.")
        if not self.textEdit_Age.text():
            self.error_messages.append("Age is empty.")
        if not self.comboBox_Gender.currentText():
            self.error_messages.append("Gender is not selected.")
        if not self.contact_number_valid():
            self.error_messages.append("Invalid Contact Number. It should be an 11-digit number.")
        if not self.email_valid():
            self.error_messages.append("Invalid Email. Please enter a valid email address.")
        if not self.comboBox_BloodGroup.currentText():
            self.error_messages.append("Blood Group is not selected.")

        return not bool(self.error_messages)

    def contact_number_valid(self):
        contact_number_pattern = r'^\d{11}$'
        return bool(re.match(contact_number_pattern, self.textEdit_ContactNumber.text()))

    def email_valid(self):
        email_pattern = r'^[\w\.-]+@[\w\.-]+$'
        return bool(re.match(email_pattern, self.textEdit_Email.text()))

    def get_error_messages(self):
        return "\n".join(self.error_messages)