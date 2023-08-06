import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class JM:
    @staticmethod
    def CreateWindow(app_title, calculate_text, calculate_function):
        app = QApplication([])
        window = QWidget()
        window.setWindowTitle(app_title)

        layout = QVBoxLayout()

        input_label = QLabel("Input:")
        input_field = QLineEdit()
        layout.addWidget(input_label)
        layout.addWidget(input_field)

        output_label = QLabel("Output:")
        output_field = QLabel()
        layout.addWidget(output_label)
        layout.addWidget(output_field)

        calculate_button = QPushButton(calculate_text)
        calculate_button.clicked.connect(lambda: JM.calculate(input_field, output_field, calculate_function))
        layout.addWidget(calculate_button)

        window.setLayout(layout)
        window.show()

        sys.exit(app.exec())

    @staticmethod
    def calculate(input_field, output_field, calculate_function):
        input_value = input_field.text()
        output_value = calculate_function(input_value)
        output_field.setText(output_value)
