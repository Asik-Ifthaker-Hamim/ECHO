import asyncio
import threading
from datetime import datetime
from typing import Callable, Optional
from .speech import speech_service
from .commands import command_service

class ListenerService:
    def __init__(self):
        self.listening_active = False
        self.is_running = False
        self.listen_thread: Optional[threading.Thread] = None
        self.status_callback: Optional[Callable] = None
        
    def set_status_callback(self, callback: Callable):
        self.status_callback = callback
    
    def _send_status(self, message: str, color: str):
        if self.status_callback:
            try:
                asyncio.run(self.status_callback({
                    "message": message,
                    "color": color,
                    "timestamp": datetime.now().isoformat(),
                    "is_listening": self.is_running,
                    "is_active": self.listening_active
                }))
            except Exception:
                pass
    
    def start_listening(self):
        if not self.is_running:
            self.is_running = True
            self.listen_thread = threading.Thread(target=self._manage_listening, daemon=True)
            self.listen_thread.start()
            self._send_status("Listening started. Say 'Hey Echo' to activate.", "blue")
    
    def stop_listening(self):
        self.is_running = False
        self.listening_active = False
        self._send_status("Listening stopped.", "red")
    
    def _toggle_listening_state(self, command: str):
        if "hey echo" in command:
            self.listening_active = True
            self._send_status("Voice recognition activated. Listening for commands.", "green")
            speech_service.speak("Voice recognition activated. Listening for commands.")
        elif "stop listening" in command:
            self.listening_active = False
            self._send_status("Voice recognition deactivated. Waiting for 'Hey Echo'.", "red")
            speech_service.speak("Voice recognition deactivated. Waiting for 'Hey Echo'.")
    
    def _manage_listening(self):
        while self.is_running:
            command = speech_service.listen_command()
            if command:
                if self.listening_active:
                    if "stop listening" in command:
                        self._toggle_listening_state(command)
                    else:
                        success, message, color = command_service.execute_command(command)
                        self._send_status(message, color)
                        if success:
                            speech_service.speak(message.replace("Opening: ", "Opening "))
                        else:
                            speech_service.speak(message)
                        self.listening_active = False
                        self._send_status("Command executed. Waiting for 'Hey Echo'.", "blue")
                else:
                    if "hey echo" in command:
                        self._toggle_listening_state(command)

listener_service = ListenerService()
