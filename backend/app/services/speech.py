import speech_recognition as sr
from typing import Optional
import threading

class SpeechService:
    def __init__(self):
        self.engine = None
        self.voices = []
        self.selected_voice = "male"
        self._lock = threading.Lock()
        self._initialized = False
        
    def _init_engine(self):
        if not self._initialized:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.voices = self.engine.getProperty('voices')
                self._initialized = True
            except Exception as e:
                print(f"Warning: TTS engine not available: {e}")
                self._initialized = True
        
    def set_voice(self, voice_type: str):
        self._init_engine()
        with self._lock:
            self.selected_voice = voice_type
            if self.engine and len(self.voices) > 0:
                if voice_type == "male" and len(self.voices) > 0:
                    self.engine.setProperty('voice', self.voices[0].id)
                elif voice_type == "female" and len(self.voices) > 1:
                    self.engine.setProperty('voice', self.voices[1].id)
    
    def speak(self, text: str):
        self._init_engine()
        if not self.engine:
            print(f"TTS not available: {text}")
            return
        with self._lock:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
    
    def listen_command(self, timeout: int = 5) -> Optional[str]:
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=timeout)
                command = recognizer.recognize_google(audio).lower()
                return command
        except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
            return None

speech_service = SpeechService()
