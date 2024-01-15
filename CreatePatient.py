import sys
import os
import json
import re
import datetime
from PyQt5.QtCore import Qt, QCoreApplication, QMetaObject
from PyQt5.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QApplication,
    QWidget,
    QMessageBox,
    QFileDialog,
)
from database import Database
from PyQt5.QtWidgets import QDialog


class CreatePatientForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Patient")
        self.resize(300, 250)
        self.initUI()
        self.db = Database()
        self.db.connect()

    def initUI(self):
        layout = QFormLayout()

        self.patient_name_input = QLineEdit()
        layout.addRow("Patient's Name:", self.patient_name_input)

        self.patient_age_input = QLineEdit()
        self.patient_age_input.setInputMask("999")
        layout.addRow("Age:", self.patient_age_input)

        self.gender_combobox = QComboBox()
        self.gender_combobox.addItems(["Male", "Female", "Other"])
        layout.addRow("Gender:", self.gender_combobox)

        self.contact_number_input = QLineEdit()
        layout.addRow("Contact Number:", self.contact_number_input)

        self.email_input = QLineEdit()
        layout.addRow("Email:", self.email_input)

        self.blood_group_combobox = QComboBox()
        self.blood_group_combobox.addItems(
            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        layout.addRow("Blood Group:", self.blood_group_combobox)

        # self.treatment_plan_text = QTextEdit()
        # layout.addRow("Treatment Plan:", self.treatment_plan_text)

        self.create_patient_button = QPushButton("Create Patient")
        layout.addRow(self.create_patient_button)
        self.create_patient_button.clicked.connect(self.generate_patient_id)

        self.setLayout(layout)

        QMetaObject.connectSlotsByName(self)

        self.patient_name_input.returnPressed.connect(
            lambda: self.focus_next(self.patient_age_input))
        self.patient_age_input.returnPressed.connect(
            lambda: self.focus_next(self.gender_combobox))
        self.gender_combobox.activated.connect(
            lambda: self.focus_next(self.contact_number_input))
        self.contact_number_input.returnPressed.connect(
            lambda: self.focus_next(self.email_input))
        self.email_input.returnPressed.connect(
            lambda: self.focus_next(self.blood_group_combobox))
        # self.blood_group_combobox.activated.connect(lambda: self.focus_next(self.treatment_plan_text))

    def focus_next(self, widget):
        widget.setFocus()

    def generate_patient_id(self):
        if self.validate_fields():
            now = datetime.datetime.now()
            year = now.year % 100
            month = now.month
            day = now.day

            gender = {"Male": 2, "Female": 1, "Other": 0}.get(
                self.gender_combobox.currentText(), 0)
            blood_group = {
                "O+": "01",
                "O-": "02",
                "A+": "11",
                "A-": "12",
                "B+": "21",
                "B-": "22",
                "AB+": "31",
                "AB-": "32",
            }.get(self.blood_group_combobox.currentText(), "00")

            phone_number = self.contact_number_input.text()[-4:]
            patient_id = f"{year:02d}{month:02d}{day:02d}-{gender}-{blood_group}-{phone_number}"

            patient_data = {
                "Patient's Name": self.patient_name_input.text(),
                "Age": self.patient_age_input.text(),
                "Gender": self.gender_combobox.currentText(),
                "Contact Number": self.contact_number_input.text(),
                "Email": self.email_input.text(),
                "Blood Group": self.blood_group_combobox.currentText(),
                # "Treatment Plan": self.treatment_plan_text.toPlainText(),
            }

            # Insert patient data into the database
            query = "INSERT INTO patient (P_ID, P_name, Age, Gender, Blood_Group, Contact_No, Email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data = (
                patient_id,
                patient_data["Patient's Name"],
                patient_data["Age"],
                patient_data["Gender"],
                patient_data["Blood Group"],
                patient_data["Contact Number"],
                patient_data["Email"],
            )
            self.db.execute_query(query, data)

            message = f"Patient has been created successfully. Patient ID: {patient_id}"
            msg_box = QMessageBox()
            msg_box.information(None, "Patient ID", message)

            default_directory = "patient_data"

            choice_msg = "Do you want to save the patient's data in the default location or choose another location?"
            choice_box = QMessageBox()
            choice_box.setIcon(QMessageBox.Question)
            choice_box.setText(choice_msg)
            choice_box.addButton(QPushButton(
                "Default Location"), QMessageBox.YesRole)
            choice_box.addButton(QPushButton(
                "Another Location"), QMessageBox.NoRole)
            user_choice = choice_box.exec_()

            if user_choice == 0:
                directory = os.path.join(os.getcwd(), default_directory)
            else:
                directory = QFileDialog.getExistingDirectory(
                    None, "Select Directory", default_directory)

            if directory:
                folder_path = os.path.join(directory, patient_id)

                if os.path.exists(folder_path):
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Question)
                    msg_box.setText(
                        "A folder with the same Patient ID already exists. Do you want to overwrite it?")
                    msg_box.setStandardButtons(
                        QMessageBox.Yes | QMessageBox.No)
                    msg_box.setDefaultButton(QMessageBox.No)
                    user_choice = msg_box.exec_()

                    if user_choice == QMessageBox.No:
                        return

                os.makedirs(folder_path, exist_ok=True)

                json_file_path = os.path.join(
                    folder_path, f"{patient_id}.json")
                with open(json_file_path, "w") as json_file:
                    json.dump(patient_data, json_file, indent=4)

                message = f"Patient has been created successfully. Patient ID: <span style='color: blue;'>{patient_id}</span>"
                msg_box = QMessageBox()
                msg_box.setTextFormat(Qt.RichText)
                msg_box.information(None, "Patient ID", message)
            else:
                msg_box = QMessageBox()
                msg_box.setText(
                    "No directory selected. Please select a directory to save the patient's data.")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setText(
                "Please correct the following errors:\n\n" + self.get_error_messages())
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.exec_()

    def validate_fields(self):
        self.error_messages = []

        if not self.patient_name_input.text():
            self.error_messages.append("Patient's Name is empty.")
        if not self.patient_age_input.text():
            self.error_messages.append("Age is empty.")
        if not self.gender_combobox.currentText():
            self.error_messages.append("Gender is not selected.")
        if not self.contact_number_valid():
            self.error_messages.append(
                "Invalid Contact Number. It should be an 11-digit number.")
        if not self.email_valid():
            self.error_messages.append(
                "Invalid Email. Please enter a valid email address.")
        if not self.blood_group_combobox.currentText():
            self.error_messages.append("Blood Group is not selected.")

        return not bool(self.error_messages)

    def contact_number_valid(self):
        contact_number_pattern = r'^\d{11}$'
        return bool(re.match(contact_number_pattern, self.contact_number_input.text()))

    def email_valid(self):
        email_pattern = r'^[\w\.-]+@[\w\.-]+$'
        return bool(re.match(email_pattern, self.email_input.text()))

    def get_error_messages(self):
        return "\n".join(self.error_messages)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CreatePatientForm()
    form.show()
    sys.exit(app.exec_())
