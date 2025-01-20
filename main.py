import os
import subprocess
import pyttsx3
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication
import threading
import sys

# Import the GUI class and Commands dictionary from the design module
from design import VoiceAssistantGUI, Commands

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

# Preset voice command dictionary
commands = {
    # Web Browsers
     "open chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "open edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "open firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    "open opera": "C:\\Program Files\\Opera\\launcher.exe",

    # Productivity Tools
    "open notepad": "notepad.exe",
    "open word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "open excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "open powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
    "open outlook": "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE",
    "open onenote": "C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE",
    "open sticky notes": "stikynot.exe",
    "open calculator": "calc.exe",

    # Communication Apps
    "open teams": "C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe",
    "open zoom": "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe",
    "open skype": "C:\\Program Files (x86)\\Microsoft\\Skype for Desktop\\Skype.exe",
    "open whatsapp": "C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\WhatsApp.exe",

    # Media Players
    "open vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
    "open spotify": "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe",
    "open windows media player": "wmplayer.exe",

    # Social Media
    "open facebook": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.facebook.com",
    "open instagram": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.instagram.com",
    "open twitter": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.twitter.com",
    "open youtube": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.youtube.com",

    # File Management
    "open file explorer": "explorer.exe",
    "open control panel": "control.exe",
    "open task manager": "taskmgr.exe",

    # Development Tools
    "open vs code": "C:/Users/Avishek Das/AppData/Local/Programs/Microsoft VS Code/Code.exe",
    "open pycharm": "C:\\Program Files\\JetBrains\\PyCharm Community Edition\\bin\\pycharm64.exe",
    "open notepad++": "C:\\Program Files\\Notepad++\\notepad++.exe",

    # Gaming
    "open steam": "C:\\Program Files (x86)\\Steam\\steam.exe",
    "open epic games": "C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe",

    # Utilities
    "open paint": "mspaint.exe",
    "open snipping tool": "snippingtool.exe",
    "open command prompt": "cmd.exe",
    "open powershell": "powershell.exe",
    "open registry editor": "regedit.exe",
    "open disk cleanup": "cleanmgr.exe",
    "open disk management": "diskmgmt.msc",
    "open device manager": "devmgmt.msc",
    "open event viewer": "eventvwr.exe",
    "open system information": "msinfo32.exe",
    "open character map": "charmap.exe",
    "open remote desktop": "mstsc.exe",

    # Cloud Storage
    "open onedrive": "C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe",
    "open google drive": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://drive.google.com",

    # Miscellaneous
    "open calendar": "outlookcal:",
    "open mail": "outlookmail:",
    "open weather": "bingweather:",
    "open news": "bingnews:",
    "open maps": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.google.com/maps",
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
    elif command in commands or command in Commands:  # Check both preset and dynamic commands
        path_or_command = commands.get(command) or Commands.get(command)
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
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            return command
        except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
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

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = VoiceAssistantGUI()
    main_window.show()
    listening_thread = threading.Thread(target=manage_listening, daemon=True)
    listening_thread.start()
    sys.exit(app.exec_())