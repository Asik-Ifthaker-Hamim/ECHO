from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLineEdit, QFileDialog, QComboBox, QMessageBox, QFrame, QStatusBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui ifrom PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLineEdit, QFileDialog, QComboBox, QMessageBox, QFrame, QStatusBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QLinearGradient, QPalette

# Define Commands dictionary here (shared with main.py)
Commands = {}

class VoiceAssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Properties
        self.setWindowTitle("Voice Command Assistant")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(self.get_background_style())

        # Main Layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Title Label
        self.label_title = QLabel("Voice Command Assistant", self)
        self.label_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("color: white;")
        self.layout.addWidget(self.label_title)

        # Status Label
        self.label_status = QLabel("Say 'Hey Echo' to activate voice recognition.", self)
        self.label_status.setFont(QFont("Segoe UI", 14))
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setStyleSheet("color: white;")
        self.layout.addWidget(self.label_status)

        # Buttons
        self.init_buttons()

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("background-color: #333; color: white; font-size: 14px;")

        # Initialize sub-windows as None
        self.set_command_window = None
        self.options_window = None

    def get_background_style(self):
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor(30, 30, 30))
        gradient.setColorAt(1, QColor(50, 50, 50))
        palette = QPalette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)
        return ""

    def init_buttons(self):
        # Bottom buttons (horizontal layout)
        bottom_frame = QFrame(self)
        bottom_frame.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 5px;")
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.setSpacing(10)

        # Set Command Button
        self.btn_set_command = QPushButton("Set Command", self)
        self.btn_set_command.setFont(QFont("Segoe UI", 14))
        self.btn_set_command.setStyleSheet(self.button_style())
        self.btn_set_command.clicked.connect(self.open_set_command_window)
        bottom_layout.addWidget(self.btn_set_command)

        # Options Button
        self.btn_options = QPushButton("Options", self)
        self.btn_options.setFont(QFont("Segoe UI", 14))
        self.btn_options.setStyleSheet(self.button_style())
        self.btn_options.clicked.connect(self.open_options_window)
        bottom_layout.addWidget(self.btn_options)

        # Exit Button
        self.btn_exit = QPushButton("Exit", self)
        self.btn_exit.setFont(QFont("Segoe UI", 14))
        self.btn_exit.setStyleSheet(self.button_style())
        self.btn_exit.clicked.connect(self.close)
        bottom_layout.addWidget(self.btn_exit)

        # Add bottom frame to the main layout
        self.layout.addWidget(bottom_frame, alignment=Qt.AlignBottom)

    def button_style(self):
        return """
            QPushButton {
                background-color: transparent;
                border: 1px solid white;
                padding: 10px 20px;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """

    def open_set_command_window(self):
        # Create the SetCommandWindow if it doesn't exist
        if self.set_command_window is None:
            self.set_command_window = SetCommandWindow()
        self.set_command_window.show()

    def open_options_window(self):
        # Create the OptionsWindow if it doesn't exist
        if self.options_window is None:
            self.options_window = OptionsWindow()
        self.options_window.show()

    def update_status(self, message, color="white"):
        self.label_status.setText(message)
        self.label_status.setStyleSheet(f"color: {color};")


class SetCommandWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set Command")
        self.setGeometry(150, 150, 400, 200)
        self.setStyleSheet(self.get_popup_style())

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Application Name Input
        layout.addWidget(QLabel("Set Command:", self))
        self.entry_app_name = QLineEdit(self)
        self.entry_app_name.setFont(QFont("Segoe UI", 14))
        self.entry_app_name.setStyleSheet(self.input_style())
        layout.addWidget(self.entry_app_name)

        # Application Path Input
        layout.addWidget(QLabel("Application Path:", self))
        self.entry_app_path = QLineEdit(self)
        self.entry_app_path.setFont(QFont("Segoe UI", 14))
        self.entry_app_path.setStyleSheet(self.input_style())
        layout.addWidget(self.entry_app_path)

        # Browse Button
        browse_layout = QHBoxLayout()
        self.btn_browse = QPushButton("Browse", self)
        self.btn_browse.setFont(QFont("Segoe UI", 14))
        self.btn_browse.setStyleSheet(self.button_style())
        self.btn_browse.clicked.connect(self.browse_file)
        browse_layout.addWidget(self.entry_app_path)
        browse_layout.addWidget(self.btn_browse)
        layout.addLayout(browse_layout)

        # Save Button
        self.btn_save = QPushButton("Save", self)
        self.btn_save.setFont(QFont("Segoe UI", 14))
        self.btn_save.setStyleSheet(self.button_style())
        self.btn_save.clicked.connect(self.save_command)
        layout.addWidget(self.btn_save)

    def get_popup_style(self):
        return """
            background-color: #333;
            color: white;
            font-family: Segoe UI;
            border-radius: 5px;
        """

    def input_style(self):
        return """
            background-color: #555;
            color: white;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Application", "", "All Files (*.*)")
        if file_path:
            self.entry_app_path.setText(file_path)

    def save_command(self):
        app_name = self.entry_app_name.text().strip()
        app_path = self.entry_app_path.text().strip()
        if app_name and app_path:
            Commands[app_name.lower()] = app_path  # Update the shared Commands dictionary
            QMessageBox.information(self, "Success", f"Command for '{app_name}' saved successfully.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Please provide both application name and path.")


class OptionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Options")
        self.setGeometry(200, 200, 300, 150)
        self.setStyleSheet(self.get_popup_style())

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Select Voice:", self))
        self.voice_choice = QComboBox(self)
        self.voice_choice.addItems(["male", "female"])
        self.voice_choice.setFont(QFont("Segoe UI", 14))
        self.voice_choice.setStyleSheet(self.input_style())
        layout.addWidget(self.voice_choice)

        # Apply Button
        self.btn_apply = QPushButton("Apply", self)
        self.btn_apply.setFont(QFont("Segoe UI", 14))
        self.btn_apply.setStyleSheet(self.button_style())
        self.btn_apply.clicked.connect(self.apply_voice)
        layout.addWidget(self.btn_apply)

    def get_popup_style(self):
        return """
            background-color: #333;
            color: white;
            font-family: Segoe UI;
            border-radius: 5px;
        """

    def input_style(self):
        return """
            background-color: #555;
            color: white;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """

    def apply_voice(self):
        selected_voice = self.voice_choice.currentText()
        # Use the set_voice function from main.py
        from main import set_voice
        set_voice(selected_voice)
        QMessageBox.information(self, "Success", f"Voice set to {selected_voice.capitalize()}.")mport QFont, QColor, QLinearGradient, QPalette
from functionality import set_voice, commands  # Import set_voice and commands

class VoiceAssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Properties
        self.setWindowTitle("Voice Command Assistant")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(self.get_background_style())

        # Main Layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Title Label
        self.label_title = QLabel("Voice Command Assistant", self)
        self.label_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("color: white;")
        self.layout.addWidget(self.label_title)

        # Status Label
        self.label_status = QLabel("Say 'Hey Echo' to activate voice recognition.", self)
        self.label_status.setFont(QFont("Segoe UI", 10))
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setStyleSheet("color: white;")
        self.layout.addWidget(self.label_status)

        # Buttons
        self.init_buttons()

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("background-color: #333; color: white; font-size: 10px;")

        # Initialize sub-windows as None
        self.set_command_window = None
        self.options_window = None

    def get_background_style(self):
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor(30, 30, 30))
        gradient.setColorAt(1, QColor(50, 50, 50))
        palette = QPalette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)
        return ""

    def init_buttons(self):
        # Bottom buttons (horizontal layout)
        bottom_frame = QFrame(self)
        bottom_frame.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 5px;")
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.setSpacing(10)

        # Set Command Button
        self.btn_set_command = QPushButton("Set Command", self)
        self.btn_set_command.setFont(QFont("Segoe UI", 10))
        self.btn_set_command.setStyleSheet(self.button_style())
        self.btn_set_command.clicked.connect(self.open_set_command_window)
        bottom_layout.addWidget(self.btn_set_command)

        # Options Button
        self.btn_options = QPushButton("Options", self)
        self.btn_options.setFont(QFont("Segoe UI", 10))
        self.btn_options.setStyleSheet(self.button_style())
        self.btn_options.clicked.connect(self.open_options_window)
        bottom_layout.addWidget(self.btn_options)

        # Exit Button
        self.btn_exit = QPushButton("Exit", self)
        self.btn_exit.setFont(QFont("Segoe UI", 10))
        self.btn_exit.setStyleSheet(self.button_style())
        self.btn_exit.clicked.connect(self.close)
        bottom_layout.addWidget(self.btn_exit)

        # Add bottom frame to the main layout
        self.layout.addWidget(bottom_frame, alignment=Qt.AlignBottom)

    def button_style(self):
        return """
            QPushButton {
                background-color: transparent;
                border: 1px solid white;
                padding: 8px 16px;
                color: white;
                border-radius: 5px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """

    def open_set_command_window(self):
        # Create the SetCommandWindow if it doesn't exist
        if self.set_command_window is None:
            self.set_command_window = SetCommandWindow()
        self.set_command_window.show()

    def open_options_window(self):
        # Create the OptionsWindow if it doesn't exist
        if self.options_window is None:
            self.options_window = OptionsWindow()
        self.options_window.show()

    def update_status(self, message, color="white"):
        self.label_status.setText(message)
        self.label_status.setStyleSheet(f"color: {color};")
        self.status_bar.showMessage(message)


class SetCommandWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set Command")
        self.setGeometry(150, 150, 400, 200)
        self.setStyleSheet(self.get_popup_style())

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Application Name Input
        layout.addWidget(QLabel("Set Command:", self))
        self.entry_app_name = QLineEdit(self)
        self.entry_app_name.setFont(QFont("Segoe UI", 10))
        self.entry_app_name.setStyleSheet(self.input_style())
        layout.addWidget(self.entry_app_name)

        # Application Path Input
        layout.addWidget(QLabel("Application Path:", self))
        self.entry_app_path = QLineEdit(self)
        self.entry_app_path.setFont(QFont("Segoe UI", 10))
        self.entry_app_path.setStyleSheet(self.input_style())
        layout.addWidget(self.entry_app_path)

        # Browse Button
        browse_layout = QHBoxLayout()
        self.btn_browse = QPushButton("Browse", self)
        self.btn_browse.setFont(QFont("Segoe UI", 10))
        self.btn_browse.setStyleSheet(self.button_style())
        self.btn_browse.clicked.connect(self.browse_file)
        browse_layout.addWidget(self.entry_app_path)
        browse_layout.addWidget(self.btn_browse)
        layout.addLayout(browse_layout)

        # Save Button
        self.btn_save = QPushButton("Save", self)
        self.btn_save.setFont(QFont("Segoe UI", 10))
        self.btn_save.setStyleSheet(self.button_style())
        self.btn_save.clicked.connect(self.save_command)
        layout.addWidget(self.btn_save)

    def get_popup_style(self):
        return """
            background-color: #333;
            color: white;
            font-family: Segoe UI;
            border-radius: 5px;
        """

    def input_style(self):
        return """
            background-color: #555;
            color: white;
            border-radius: 5px;
            padding: 5px;
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Application", "", "All Files (*.*)")
        if file_path:
            self.entry_app_path.setText(file_path)

    def save_command(self):
        app_name = self.entry_app_name.text().strip()
        app_path = self.entry_app_path.text().strip()
        if app_name and app_path:
            commands[app_name.lower()] = app_path  # Update the commands dictionary
            QMessageBox.information(self, "Success", f"Command for '{app_name}' saved successfully.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Please provide both application name and path.")


class OptionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Options")
        self.setGeometry(200, 200, 300, 150)
        self.setStyleSheet(self.get_popup_style())

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Select Voice:", self))
        self.voice_choice = QComboBox(self)
        self.voice_choice.addItems(["male", "female"])
        self.voice_choice.setFont(QFont("Segoe UI", 10))
        self.voice_choice.setStyleSheet(self.input_style())
        layout.addWidget(self.voice_choice)

        # Apply Button
        self.btn_apply = QPushButton("Apply", self)
        self.btn_apply.setFont(QFont("Segoe UI", 10))
        self.btn_apply.setStyleSheet(self.button_style())
        self.btn_apply.clicked.connect(self.apply_voice)
        layout.addWidget(self.btn_apply)

    def get_popup_style(self):
        return """
            background-color: #333;
            color: white;
            font-family: Segoe UI;
            border-radius: 5px;
        """

    def input_style(self):
        return """
            background-color: #555;
            color: white;
            border-radius: 5px;
            padding: 5px;
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """

    def apply_voice(self):
        selected_voice = self.voice_choice.currentText()
        set_voice(selected_voice)  # Use the imported set_voice function
        QMessageBox.information(self, "Success", f"Voice set to {selected_voice.capitalize()}.")