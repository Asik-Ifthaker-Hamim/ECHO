import sys
import threading
from PyQt5.QtWidgets import QApplication
from design import VoiceAssistantGUI
from functionality import manage_listening, set_voice, commands, execute_command, toggle_listening_state, speak

# Main function to start the application
def start_voice_assistant():
    # Create the application instance
    app = QApplication(sys.argv)

    # Initialize the main window
    main_window = VoiceAssistantGUI()
    main_window.show()

    # Start the listening thread
    listening_thread = threading.Thread(target=manage_listening, daemon=True)
    listening_thread.start()

    # Connect GUI signals to functionality
    main_window.btn_set_command.clicked.connect(main_window.open_set_command_window)
    main_window.btn_options.clicked.connect(main_window.open_options_window)
    main_window.btn_exit.clicked.connect(main_window.close)

    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_voice_assistant()