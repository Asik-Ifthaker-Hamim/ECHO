import os
import subprocess
import pyttsx3
import speech_recognition as sr
import threading

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Available voices
voices = engine.getProperty('voices')

# Default voice selection
selected_voice = "male"

# Function to set the voice
def set_voice(voice_type):
    global selected_voice
    selected_voice = voice_type
    if voice_type == "male":
        engine.setProperty('voice', voices[0].id)  # Male voice
    else:
        engine.setProperty('voice', voices[1].id)  # Female voice
    print(f"Voice set to: {voice_type}")

# Voice command dictionary
commands = {
    "open chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "open notepad": "notepad.exe",
    "open calculator": "calc.exe",
    "open editor": "C:\\Users\\USER\\AppData\\Local\\CapCut\\Apps\\CapCut.exe --src3",
    "open edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "open task manager": "C:\\Windows\\System32\\Taskmgr.exe",
}

# Function for text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to execute the command
def execute_command(command):
    if "find" in command:
        search_item = command.replace("find ", "")
        search_and_open(search_item)
    elif command in commands:
        path_or_command = commands[command]
        try:
            if isinstance(path_or_command, list):
                subprocess.Popen(path_or_command)
            else:
                subprocess.Popen(path_or_command)
            app_name = command.replace("open ", "")
            main_window.update_status(f"Opening: {app_name}", "green")
            speak(f"Opening {app_name}...")
        except Exception as e:
            main_window.update_status(f"Error: {str(e)}", "red")
            speak("Error opening the application.")
    else:
        main_window.update_status("Command not recognized.", "red")
        speak("Command not recognized.")

# Function to search and open a folder or file
def search_and_open(target_name):
    main_window.update_status("Searching, this may take a moment...", "blue")
    speak("Searching, this may take a moment.")
    found_paths = []

    for root_dir, dirs, files in os.walk("C:\\"):
        for folder in dirs:
            if target_name.lower() in folder.lower():
                found_paths.append(os.path.join(root_dir, folder))
        for file in files:
            if target_name.lower() in file.lower():
                found_paths.append(os.path.join(root_dir, file))

    if found_paths:
        target_path = found_paths[0]  # Open the first found result
        speak(f"Opening {target_name}.")
        main_window.update_status(f"Opening: {target_path}", "green")
        subprocess.Popen(f'explorer "{target_path}"')
    else:
        main_window.update_status(f"'{target_name}' not found.", "red")
        speak(f"Sorry, I could not find {target_name}.")

# Function for listening to the command
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
            return ""

# Listening state
listening_active = False

# Function to toggle the listening state
def toggle_listening_state(command):
    global listening_active
    if "hey echo" in command:
        listening_active = True
        main_window.update_status("Voice recognition activated. Listening for commands.", "green")
        speak("Voice recognition activated. Listening for commands.")
    elif "stop listening" in command:
        listening_active = False
        main_window.update_status("Voice recognition deactivated. Waiting for 'Hey Echo'.", "red")
        speak("Voice recognition deactivated. Waiting for 'Hey Echo'.")

# Function to listen continuously
def manage_listening():
    global listening_active
    while True:
        command = listen_command()
        if listening_active:
            if command:
                if "stop listening" in command:
                    toggle_listening_state(command)
                else:
                    execute_command(command)
                    listening_active = False
                    main_window.update_status("Command executed. Waiting for 'Hey Echo'.", "red")
        else:
            if "hey echo" in command:
                toggle_listening_state(command)

# Main function to start the application
def start_voice_assistant():
    global main_window
    from PyQt5.QtWidgets import QApplication
    from design import VoiceAssistantGUI

    app = QApplication([])
    main_window = VoiceAssistantGUI()
    main_window.show()

    # Start the listening thread
    listening_thread = threading.Thread(target=manage_listening, daemon=True)
    listening_thread.start()

    app.exec_()

if __name__ == "__main__":
    start_voice_assistant()