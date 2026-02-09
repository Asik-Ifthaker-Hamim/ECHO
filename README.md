# ECHO – Efficient Command Handling Operator 🌐

ECHO is an intelligent voice assistant with a modern desktop interface. Version 2.0 features a complete architectural upgrade with a FastAPI backend and React-based frontend, providing a responsive and efficient user experience.

## Features 🔧

- **Voice Recognition:** 🎤 Hands-free control with wake word activation ("Hey Echo")
- **Command Execution:** ⏳ Launch applications, open files, and execute custom commands
- **Persistent Storage:** 💾 SQLite database for custom commands and settings
- **Real-time Status Updates:** 🔄 WebSocket connection for instant feedback
- **Modern UI:** 🎨 React-based interface with dark theme
- **Customizable:** 🔧 Add, edit, and manage voice commands
- **Voice Options:** 🎵 Choose between male and female TTS voices

## Architecture

### Backend (FastAPI)
- **Framework:** FastAPI with WebSocket support
- **Database:** SQLite for persistence
- **Services:** Modular speech recognition, command execution, and listening management
- **API:** RESTful endpoints + WebSocket for real-time updates

### Frontend (React + Vite)
- **UI Framework:** React with functional components and hooks
- **Build Tool:** Vite for fast development and optimized builds
- **Styling:** Custom CSS with modern design patterns
- **Communication:** REST API + WebSocket for real-time status

## Installation 🛠️

### Prerequisites
- Python 3.12+
- Node.js 18+
- Microphone access

### 1. Clone the Repository

```bash
git clone https://github.com/Asik-Ifthaker-Hamim/ECHO.git
cd ECHO
```

### 2. Install Python Dependencies

```bash
# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 3. Install Node Dependencies

```bash
npm install
```

## Usage 🎮

### Running the Application

#### Option 1: Run Backend and Frontend Separately

**Terminal 1 - Start Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
npm run dev:vite
```

Then open your browser to `http://localhost:5173`

#### Option 2: Run Everything Together (Requires concurrently)

```bash
npm run dev
```

### Using the Legacy PyQt5 Interface

The original PyQt5 interface is still available:

```bash
python main.py
```

## How to Use

1. **Start the application** using one of the methods above
2. **Click "Start Listening"** in the UI
3. **Say "Hey Echo"** to activate voice recognition
4. **Give a voice command** (e.g., "open notepad", "find documents")
5. **Say "stop listening"** to deactivate voice recognition

### Adding Custom Commands

**Via UI:**
1. Enter the command name (e.g., "open myapp")
2. Enter the application path
3. Click "Add Command"

**Supported Command Types:**
- **Application Launch:** `open chrome` → launches Chrome
- **File Search:** `find myfile` → searches and opens the file
- **Web Apps:** Commands can launch browser apps with specific URLs

## API Documentation

Once the backend is running, visit:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Key Endpoints

- `GET /commands/` - List all commands
- `POST /commands/` - Create a new command
- `DELETE /commands/{name}` - Delete a command
- `POST /listener/start` - Start voice listening
- `POST /listener/stop` - Stop voice listening
- `WS /listener/ws` - WebSocket for real-time status updates
- `GET /settings/` - Get all settings
- `POST /settings/{key}` - Update a setting

## Project Structure

```
ECHO/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── models/        # Database models and schemas
│   │   ├── services/      # Business logic (speech, commands, listener)
│   │   └── main.py        # FastAPI application
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   ├── styles/        # CSS files
│   │   ├── App.jsx        # Main React component
│   │   └── main.jsx       # React entry point
│   └── index.html
├── main.py                # Legacy PyQt5 application
├── design.py              # Legacy PyQt5 UI definitions
├── vite.config.js         # Vite configuration
├── package.json           # Node dependencies and scripts
└── README.md
```

## Configuration

### Default Settings
- **Voice:** Male (changeable in UI)
- **Wake Phrase:** "hey echo"
- **Backend Port:** 8000
- **Frontend Port:** 5173

### Database
- Location: `backend/echo.db`
- Auto-created on first run
- Stores custom commands and settings

## Development

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Development

```bash
npm run dev:vite
```

The frontend will hot-reload on changes.

## Troubleshooting

### Microphone Issues
- Ensure microphone permissions are granted
- Check that PyAudio is properly installed
- On Linux, you may need to install PortAudio: `sudo apt-get install portaudio19-dev`

### Backend Connection Errors
- Verify the backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Ensure no firewall is blocking local connections

### Command Not Recognized
- Check that the command exists in the database
- Verify the command path is correct and accessible
- Custom commands are case-sensitive

## Contributing 📚

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add new feature'`
5. Push to the branch: `git push origin feature-branch-name`
6. Open a pull request explaining your changes

## License 🛤

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements 🌟

- Speech recognition powered by Google Speech Recognition API
- Text-to-speech powered by pyttsx3
- Modern UI inspired by Microsoft Fluent Design
- Thanks to all contributors and the open-source community

## Changelog

### Version 2.0.0
- ✨ Complete architectural redesign with FastAPI backend
- 🎨 New React-based frontend with modern UI
- 💾 SQLite database for persistent storage
- 🔄 Real-time WebSocket updates
- 📱 Responsive design
- 🔧 RESTful API with comprehensive documentation
- 🎵 Voice customization (male/female)
- ✅ Improved error handling and user feedback

### Version 1.0.0
- 🎤 Basic voice recognition
- 🖥️ PyQt5 desktop interface
- 📋 Preset command library
- 🔍 File search functionality
