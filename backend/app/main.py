from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .models.database import init_db
from .models.repository import CommandRepository, SettingsRepository
from .api import commands, settings, listener

PRESET_COMMANDS = {
    "open chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "open edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "open firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    "open opera": "C:\\Program Files\\Opera\\launcher.exe",
    "open notepad": "notepad.exe",
    "open word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "open excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "open powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
    "open outlook": "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE",
    "open onenote": "C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE",
    "open sticky notes": "stikynot.exe",
    "open calculator": "calc.exe",
    "open teams": "C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe",
    "open zoom": "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe",
    "open skype": "C:\\Program Files (x86)\\Microsoft\\Skype for Desktop\\Skype.exe",
    "open whatsapp": "C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
    "open vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
    "open spotify": "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe",
    "open windows media player": "wmplayer.exe",
    "open facebook": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.facebook.com",
    "open instagram": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.instagram.com",
    "open twitter": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.twitter.com",
    "open youtube": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.youtube.com",
    "open file explorer": "explorer.exe",
    "open control panel": "control.exe",
    "open task manager": "taskmgr.exe",
    "open vs code": "C:/Users/Avishek Das/AppData/Local/Programs/Microsoft VS Code/Code.exe",
    "open pycharm": "C:\\Program Files\\JetBrains\\PyCharm Community Edition\\bin\\pycharm64.exe",
    "open notepad++": "C:\\Program Files\\Notepad++\\notepad++.exe",
    "open steam": "C:\\Program Files (x86)\\Steam\\steam.exe",
    "open epic games": "C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe",
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
    "open onedrive": "C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe",
    "open google drive": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://drive.google.com",
    "open calendar": "outlookcal:",
    "open mail": "outlookmail:",
    "open weather": "bingweather:",
    "open news": "bingnews:",
    "open maps": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --app=https://www.google.com/maps",
}

def seed_preset_commands():
    existing_commands = {cmd["command_name"] for cmd in CommandRepository.get_all()}
    
    for cmd_name, cmd_path in PRESET_COMMANDS.items():
        if cmd_name not in existing_commands:
            CommandRepository.create(cmd_name, cmd_path, is_preset=True)

def seed_default_settings():
    if SettingsRepository.get("voice") is None:
        SettingsRepository.set("voice", "male")
    if SettingsRepository.get("wake_phrase") is None:
        SettingsRepository.set("wake_phrase", "hey echo")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_preset_commands()
    seed_default_settings()
    yield

app = FastAPI(
    title="ECHO API",
    description="Backend API for ECHO voice assistant",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(commands.router)
app.include_router(settings.router)
app.include_router(listener.router)

@app.get("/")
async def root():
    return {"message": "ECHO API is running", "version": "2.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
