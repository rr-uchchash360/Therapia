import sys
import json
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


class ExistingPatientForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Patient")
        self.resize(300, 50)
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.id_input = QLineEdit()
        layout.addRow("Patient ID:", self.id_input)

        self.select_patient_button = QPushButton("Show Data")
        layout.addRow(self.select_patient_button)
       # self.select_patient_button.clicked.connect(self.generate_patient_id)

        self.setLayout(layout)

    def showPatientInfo(self):
        patient_id = self.id_input.text()

        if not patient_id:
            QMessageBox.warning(
                self, "Warning", "Please enter a Patient ID.")
            return

        patient_data = self.fetch_patient_data(patient_id)
        self.display_patient_info(patient_data)

    def fetch_patient_data(self, patient_id):

        try:
            with open(f"{patient_id}.json", "r") as json_file:
                patient_data = json.load(json_file)
            return patient_data
        except FileNotFoundError:
            return None

    def display_patient_info(self, patient_data):
        if patient_data:
            QMessageBox.information(
                self, "Patient Data", f"Patient Name: {patient_data.get('Patient''s Name', 'N/A')}")
        else:
            QMessageBox.warning(
                self, "Patient Not Found", "Patient data not found.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ExistingPatientForm()
    form.show()
    sys.exit(app.exec_())
