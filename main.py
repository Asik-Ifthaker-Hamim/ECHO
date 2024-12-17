import os
import sys
import subprocess
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Label, Entry, Frame
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

# Voice command dictionary
commands = {
    "open chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "open notepad": "notepad.exe",
    "open calculator": "calc.exe",
    "open valorant": [
        "C:\\Riot Games\\Riot Client\\RiotClientServices.exe",
        "--launch-product=valorant",
        "--launch-patchline=live"
    ],
    "open fifa": "C:\\Program Files\\Electronic Arts\\EA Desktop\\EA Desktop\\EADesktop.exe",
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
            update_status(f"Opening: {app_name}", "green")
            speak(f"Opening {app_name}...")
        except Exception as e:
            update_status(f"Error: {str(e)}", "red")
            speak("Error opening the application.")
    else:
        update_status("Command not recognized.", "red")
        speak("Command not recognized.")

# Function to search and open a folder or file
def search_and_open(target_name):
    update_status("Searching, this may take a moment...", "blue")
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
        update_status(f"Opening: {target_path}", "green")
        subprocess.Popen(f'explorer "{target_path}"')
    else:
        update_status(f"'{target_name}' not found.", "red")
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

# Function to update the status label dynamically
def update_status(message, color="black"):
    label_status.config(text=message, foreground=color)

# GUI Setup
root = tk.Tk()
root.title("Voice Command Assistant")
root.geometry("600x450")
root.configure(bg="#f0f0f0")
root.resizable(False, False)

# Modern Styling
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat")
style.map("TButton", background=[("active", "#4CAF50")])

# Title Label
label_title = Label(root, text="Voice Command Assistant", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
label_title.pack(pady=10)

# Status Label
label_status = Label(root, text="Say 'Hey Echo' to activate voice recognition.", font=("Arial", 12), bg="#f0f0f0", fg="blue")
label_status.pack(pady=10)

# Set Command Button
def set_command():
    def save_command():
        app_name = entry_app_name.get().strip()
        app_path = entry_app_path.get().strip()
        if app_name and app_path:
            commands[app_name.lower()] = app_path
            update_status(f"Command for '{app_name}' saved successfully.", "green")
            speak(f"Command for {app_name} saved successfully.")
            command_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please provide both application name and path.")

    def browse_file():
        file_path = filedialog.askopenfilename(title="Select Application")
        if file_path:
            entry_app_path.delete(0, tk.END)
            entry_app_path.insert(0, file_path)

    command_window = tk.Toplevel(root)
    command_window.title("Set Command")
    command_window.geometry("450x250")
    command_window.configure(bg="#f0f0f0")

    # Set command (changed from "Application name")
    Label(command_window, text="Set command:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
    entry_app_name = Entry(command_window, font=("Arial", 12), width=20)
    entry_app_name.pack(pady=5)

    # Application path
    Label(command_window, text="Application path:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

    # Frame to organize the "Browse" button beside the path field
    frame = Frame(command_window, bg="#f0f0f0")
    frame.pack(pady=5)

    entry_app_path = Entry(frame, font=("Arial", 12), width=20)
    entry_app_path.pack(side="left", padx=10)

    browse_button = ttk.Button(frame, text="Browse", command=browse_file)
    browse_button.pack(side="left")

    # Save Button
    save_button = ttk.Button(command_window, text="Save", command=save_command)
    save_button.pack(pady=10)

# Set Command Button
btn_set_command = ttk.Button(root, text="Set Command", command=set_command)
btn_set_command.pack(pady=20)

# Options Menu
def open_options():
    def apply_voice():
        selected = voice_choice.get()
        set_voice(selected)
        update_status(f"Voice set to: {selected.capitalize()}", "green")
        speak(f"Voice set to {selected}.")

    options_window = tk.Toplevel(root)
    options_window.title("Options")
    options_window.geometry("300x150")
    options_window.configure(bg="#f0f0f0")

    Label(options_window, text="Select Voice:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
    voice_choice = ttk.Combobox(options_window, values=["male", "female"], font=("Arial", 12))
    voice_choice.set(selected_voice)
    voice_choice.pack(pady=5)

    apply_button = ttk.Button(options_window, text="Apply", command=apply_voice)
    apply_button.pack(pady=10)

btn_options = ttk.Button(root, text="Options", command=open_options)
btn_options.pack(pady=10)

# Exit Button
btn_exit = ttk.Button(root, text="Exit", command=root.quit)
btn_exit.pack(pady=20)

# Listening state
listening_active = False

# Function to toggle the listening state
def toggle_listening_state(command):
    global listening_active
    if "hey echo" in command:
        listening_active = True
        update_status("Voice recognition activated. Listening for commands.", "green")
        speak("Voice recognition activated. Listening for commands.")
    elif "stop listening" in command:
        listening_active = False
        update_status("Voice recognition deactivated. Waiting for 'Hey Echo'.", "red")
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
                    update_status("Command executed. Waiting for 'Hey Echo'.", "red")
        else:
            if "hey echo" in command:
                toggle_listening_state(command)
        root.update()

# Run background listening thread
def run_listening_thread():
    listening_thread = threading.Thread(target=manage_listening)
    listening_thread.daemon = True
    listening_thread.start()

if __name__ == "__main__":
    run_listening_thread()
    root.mainloop()
