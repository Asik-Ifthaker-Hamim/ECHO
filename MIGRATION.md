# Migration Guide: ECHO v1.0 to v2.0

This guide helps existing ECHO v1.0 users migrate to the new v2.0 architecture.

## What's Changing?

### Architecture
- **v1.0:** Monolithic PyQt5 desktop application
- **v2.0:** FastAPI backend + React web frontend

### Storage
- **v1.0:** In-memory only (commands lost on restart)
- **v2.0:** SQLite database (persistent storage)

### Interface
- **v1.0:** PyQt5 native desktop window
- **v2.0:** Web browser-based UI (can be wrapped in Electron)

## Before You Migrate

### Save Your Custom Commands
1. Open the old ECHO v1.0 application
2. Write down all custom commands you've added via "Set Command"
3. Note the exact command names and paths
4. Keep this list handy for re-entry in v2.0

### Check System Requirements
**Required:**
- Python 3.12 or higher
- Node.js 18 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Microphone access

**Optional (for TTS):**
- Windows: Built-in SAPI5 (included)
- macOS: Built-in NSSpeechSynthesizer (included)
- Linux: espeak or espeak-ng (`sudo apt install espeak-ng`)

## Migration Steps

### Step 1: Backup Current Installation
```bash
# Navigate to ECHO directory
cd /path/to/ECHO

# Create backup (optional)
cp -r . ../ECHO-v1-backup
```

### Step 2: Pull Latest Changes
```bash
git pull origin main
# or
git fetch origin
git checkout <new-branch-name>
```

### Step 3: Install Backend Dependencies
```bash
# Create Python virtual environment
python3 -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### Step 4: Install Frontend Dependencies
```bash
npm install
```

### Step 5: Start the New Application

**Option A: Quick Start (Recommended)**
```bash
# Windows:
start.bat

# macOS/Linux:
./start.sh
```

**Option B: Manual Start**
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend
npm run dev:vite
```

**Option C: Use Legacy PyQt5 App (No Migration)**
```bash
python main.py
```

### Step 6: Access the Web UI
Open your browser to: **http://localhost:5173**

### Step 7: Verify Preset Commands
1. Click anywhere in the UI to wake it up
2. Scroll through the Commands list
3. All 50+ preset commands should be visible

### Step 8: Re-add Custom Commands
For each custom command you saved in Step 1:

1. In the "Add New Command" section
2. Enter the command name (e.g., "open myapp")
3. Enter the application path
4. Click "Add Command"

### Step 9: Configure Settings
1. Go to the Settings panel
2. Choose your preferred voice (Male/Female)
3. Settings are saved automatically

### Step 10: Test Voice Recognition
1. Click "Start Listening"
2. Say "Hey Echo"
3. Say a command (e.g., "open calculator")
4. Verify the command executes

## Troubleshooting Migration Issues

### "Cannot find module" errors (Python)
```bash
pip install -r backend/requirements.txt
```

### "Cannot find module" errors (Node)
```bash
npm install
```

### Backend won't start
```bash
# Check if port 8000 is in use
# Windows:
netstat -ano | findstr :8000
# macOS/Linux:
lsof -i :8000

# Kill the process if needed
# Then restart the backend
```

### Frontend won't start
```bash
# Check if port 5173 is in use
# Windows:
netstat -ano | findstr :5173
# macOS/Linux:
lsof -i :5173

# Kill the process if needed
# Then restart with: npm run dev:vite
```

### TTS not working (Linux)
```bash
sudo apt update
sudo apt install espeak-ng
```

### Microphone not recognized
**Windows:**
1. Settings → Privacy → Microphone
2. Allow apps to access microphone
3. Restart browser

**macOS:**
1. System Preferences → Security & Privacy → Microphone
2. Enable for your browser
3. Restart browser

**Linux:**
```bash
# Check if mic is detected
arecord -l

# Install ALSA utils if needed
sudo apt install alsa-utils

# Test microphone
arecord --duration=3 test.wav
aplay test.wav
```

### Database errors
```bash
# Delete database and restart (will lose custom commands)
cd backend
rm echo.db
# Restart backend - database will be recreated
```

## Feature Comparison

| Feature | v1.0 (PyQt5) | v2.0 (Web) |
|---------|--------------|------------|
| Voice recognition | ✅ | ✅ |
| Command execution | ✅ | ✅ |
| File search | ✅ | ✅ |
| Custom commands | ✅ In-memory | ✅ Persistent |
| Voice settings | ✅ | ✅ |
| Preset commands | ✅ 50+ | ✅ 50+ |
| Wake word | ✅ | ✅ |
| TTS feedback | ✅ | ✅ |
| Status display | ✅ | ✅ Real-time |
| UI theme | Light | Dark |
| Storage | None | SQLite |
| API access | ❌ | ✅ |
| Documentation | ❌ | ✅ Swagger |
| Hot reload | ❌ | ✅ |
| Remote access | ❌ | ⚠️ Local only |

## Rolling Back to v1.0

If you need to go back to the old version:

### Option 1: Use Git
```bash
git checkout <old-commit-hash>
# or
git checkout v1.0-tag
```

### Option 2: Run Legacy App
The old PyQt5 app is still included:
```bash
python main.py
```

### Option 3: Restore Backup
```bash
cd ..
rm -rf ECHO
mv ECHO-v1-backup ECHO
cd ECHO
```

## Data Export/Import (Future)

Currently, there's no automatic export/import for custom commands. This feature is planned for a future release.

**Workaround for now:**
1. Manually note down custom commands
2. Re-enter them in v2.0
3. Or directly edit the SQLite database:

```bash
cd backend
sqlite3 echo.db
# INSERT INTO commands (command_name, command_path) VALUES ('open myapp', 'C:\Path\To\App.exe');
```

## Getting Help

### Documentation
- **Quick Start:** See `QUICKSTART.md`
- **Developer Guide:** See `DEVELOPMENT.md`
- **Full README:** See `README.md`
- **Upgrade Summary:** See `UPGRADE_SUMMARY.md`

### Common Issues
1. **Port conflicts:** Stop other services on ports 8000 or 5173
2. **Permission errors:** Run with proper permissions or use virtual environment
3. **Microphone access:** Grant browser microphone permissions
4. **TTS not working:** Install system TTS engine (espeak-ng on Linux)

### Support Channels
- **GitHub Issues:** Report bugs and request features
- **API Docs:** http://localhost:8000/docs (when backend running)

## FAQ

**Q: Can I use both v1.0 and v2.0?**
A: Yes! Run `python main.py` for v1.0 or use the web UI for v2.0.

**Q: Will my custom commands transfer automatically?**
A: No, you need to re-add them in the web UI. They're stored in SQLite now.

**Q: Can I access the UI from another computer?**
A: By default, no (security). You can modify `backend/app/main.py` to allow this.

**Q: Do I need to keep a terminal open?**
A: Yes, for now. An Electron wrapper can be added later for a standalone app.

**Q: Is my data synced to the cloud?**
A: No, everything is local. Your commands are stored in `backend/echo.db`.

**Q: Can I export my commands?**
A: Not via UI yet. You can copy the `echo.db` file as a backup.

**Q: What happened to the PyQt5 dependency?**
A: It's still in `requirements.txt` for backward compatibility. The web UI doesn't use it.

**Q: Can I run this on a Raspberry Pi?**
A: Probably! Install the dependencies and try it. Performance may vary.

**Q: Is Electron support planned?**
A: Yes, it can be added. The web UI is Electron-ready.

**Q: Can I customize the UI colors?**
A: Yes! Edit `frontend/src/styles/index.css` and change the CSS variables.

## Post-Migration Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] All preset commands are visible
- [ ] Custom commands re-added
- [ ] Voice settings configured
- [ ] "Start Listening" works
- [ ] Wake word ("Hey Echo") works
- [ ] Command execution works
- [ ] TTS feedback works
- [ ] Settings persist after restart
- [ ] Custom commands persist after restart

## Success!

Once all checklist items are complete, you've successfully migrated to ECHO v2.0! 🎉

Enjoy the new features:
- ✅ Persistent command storage
- ✅ Modern web interface
- ✅ Real-time status updates
- ✅ RESTful API
- ✅ Better error handling
- ✅ Comprehensive documentation

Welcome to ECHO v2.0!
