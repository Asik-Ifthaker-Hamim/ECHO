# ECHO Quick Start Guide

## First Time Setup

### 1. Install Prerequisites

**Windows:**
- Python 3.12+ from [python.org](https://www.python.org/downloads/)
- Node.js 18+ from [nodejs.org](https://nodejs.org/)

**macOS:**
```bash
brew install python@3.12 node
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.12 python3-pip nodejs npm portaudio19-dev
```

### 2. Clone and Setup

```bash
git clone https://github.com/Asik-Ifthaker-Hamim/ECHO.git
cd ECHO
```

### 3. Quick Start

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
./start.sh
```

Or manually:

```bash
# Install Python dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt

# Install Node dependencies
npm install

# Start backend (Terminal 1)
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Start frontend (Terminal 2)
npm run dev:vite
```

### 4. Access the Application

Open your browser to: **http://localhost:5173**

## Using ECHO

### Basic Workflow

1. **Click "Start Listening"** in the UI
2. **Say "Hey Echo"** (wake word)
3. **Give a command:**
   - "open chrome"
   - "open calculator"
   - "find documents"
4. **Deactivate:** Say "stop listening"

### Adding Custom Commands

1. Go to the "Add New Command" section
2. Enter command name: `open myapp`
3. Enter path: `C:\Path\To\Your\App.exe`
4. Click "Add Command"

### Voice Settings

Change the TTS voice in the Settings panel:
- Male (default)
- Female

## Example Commands

### Built-in Commands

- `open chrome` - Launch Google Chrome
- `open notepad` - Open Notepad
- `open calculator` - Open Calculator
- `open file explorer` - Open File Explorer
- `find downloads` - Search for Downloads folder

### Web Apps

- `open youtube` - Open YouTube
- `open facebook` - Open Facebook
- `open google drive` - Open Google Drive

### File Search

- `find myfile` - Searches entire C:\ drive (or home directory on Unix)

## Troubleshooting

### "Module not found" errors
```bash
pip install -r backend/requirements.txt
```

### "npm not found"
Install Node.js from [nodejs.org](https://nodejs.org/)

### Microphone not working
- Check system microphone permissions
- Ensure microphone is not muted
- Windows: Settings → Privacy → Microphone
- macOS: System Preferences → Security & Privacy → Microphone

### Backend connection failed
- Verify backend is running on port 8000
- Check http://localhost:8000/health
- Restart backend server

### Can't hear TTS voice
- Check system volume
- Ensure speakers/headphones are connected
- Verify pyttsx3 is installed: `pip show pyttsx3`

## Advanced Usage

### Custom Wake Phrase

Edit `backend/app/main.py` and modify:
```python
SettingsRepository.set("wake_phrase", "your custom phrase")
```

### Custom Command Patterns

Commands support:
- Direct executables: `notepad.exe`
- Full paths: `C:\Program Files\App\app.exe`
- Web URLs: `chrome.exe --app=https://example.com`
- Arguments: `cmd.exe /c "echo Hello"`

### API Access

Swagger documentation: http://localhost:8000/docs

Example API call:
```bash
curl -X POST http://localhost:8000/listener/start
```

## Development Mode

### Backend Hot Reload
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Hot Reload
```bash
npm run dev:vite
```

Changes to React components will auto-refresh the browser.

## Next Steps

- ✅ Add your frequently used applications
- ✅ Customize the voice settings
- ✅ Explore the preset commands
- ✅ Try the file search feature
- ✅ Check out the API documentation

## Getting Help

- **Issues:** [GitHub Issues](https://github.com/Asik-Ifthaker-Hamim/ECHO/issues)
- **Documentation:** See README.md for detailed information
- **API Docs:** http://localhost:8000/docs (when running)

Enjoy using ECHO! 🎤
