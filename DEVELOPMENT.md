# ECHO Development Guide

## Architecture Overview

ECHO v2.0 uses a modern separated architecture:

```
┌─────────────────┐      HTTP/WS     ┌──────────────────┐
│  React Frontend │ ◄──────────────► │  FastAPI Backend │
│   (Port 5173)   │                  │   (Port 8000)    │
└─────────────────┘                  └──────────────────┘
                                              │
                                              ▼
                                     ┌─────────────────┐
                                     │ SQLite Database │
                                     │   (echo.db)     │
                                     └─────────────────┘
```

## Backend Structure

### Directory Layout

```
backend/
├── app/
│   ├── api/
│   │   ├── commands.py     # Command CRUD endpoints
│   │   ├── settings.py     # Settings management
│   │   └── listener.py     # Voice listening & WebSocket
│   ├── models/
│   │   ├── database.py     # SQLite connection & init
│   │   ├── schemas.py      # Pydantic models
│   │   └── repository.py   # Data access layer
│   ├── services/
│   │   ├── speech.py       # TTS & STT services
│   │   ├── commands.py     # Command execution logic
│   │   └── listener.py     # Listening state management
│   └── main.py             # FastAPI app & startup
└── requirements.txt
```

### Key Components

#### Services Layer
- **SpeechService**: Handles text-to-speech and speech-to-text
- **CommandService**: Executes commands and searches files
- **ListenerService**: Manages listening state and wake word detection

#### API Layer
- RESTful endpoints for CRUD operations
- WebSocket endpoint for real-time status updates
- CORS middleware for frontend communication

#### Models Layer
- **Database**: SQLite connection management
- **Schemas**: Pydantic models for validation
- **Repository**: Data access patterns

### Adding New Features

#### 1. Add a New API Endpoint

```python
# backend/app/api/my_feature.py
from fastapi import APIRouter

router = APIRouter(prefix="/my-feature", tags=["my-feature"])

@router.get("/")
async def get_feature():
    return {"message": "Hello from my feature"}
```

Register in `main.py`:
```python
from .api import my_feature
app.include_router(my_feature.router)
```

#### 2. Add a New Service

```python
# backend/app/services/my_service.py
class MyService:
    def do_something(self):
        # Your logic here
        pass

my_service = MyService()
```

#### 3. Add Database Tables

```python
# backend/app/models/database.py
def init_db():
    # ... existing tables ...
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS my_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL
        )
    """)
```

## Frontend Structure

### Directory Layout

```
frontend/
├── src/
│   ├── components/
│   │   ├── StatusDisplay.jsx    # Status indicator
│   │   ├── CommandList.jsx      # Command grid
│   │   ├── CommandForm.jsx      # Add command form
│   │   └── SettingsPanel.jsx    # Settings UI
│   ├── services/
│   │   └── api.js               # API client
│   ├── styles/
│   │   ├── index.css            # Global styles
│   │   └── App.css              # Component styles
│   ├── App.jsx                  # Main component
│   └── main.jsx                 # React entry point
└── index.html
```

### Key Patterns

#### Component Structure
```jsx
import { useState, useEffect } from 'react'

const MyComponent = ({ prop1, prop2 }) => {
  const [state, setState] = useState(initialValue)
  
  useEffect(() => {
    // Side effects here
  }, [dependencies])
  
  return (
    <div className="my-component">
      {/* JSX here */}
    </div>
  )
}

export default MyComponent
```

#### API Client Usage
```javascript
import { apiClient } from './services/api'

// In component
const loadData = async () => {
  try {
    const data = await apiClient.getCommands()
    setCommands(data)
  } catch (error) {
    console.error('Error:', error)
  }
}
```

#### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/listener/ws')

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  // Handle message
}

// Clean up
return () => ws.close()
```

### Adding New Features

#### 1. Create New Component

```jsx
// frontend/src/components/MyComponent.jsx
const MyComponent = ({ data }) => {
  return (
    <div className="my-component">
      <h2>{data.title}</h2>
      <p>{data.description}</p>
    </div>
  )
}

export default MyComponent
```

#### 2. Add API Method

```javascript
// frontend/src/services/api.js
export const apiClient = {
  // ... existing methods ...
  
  async getMyData() {
    const response = await fetch(`${API_BASE_URL}/my-feature/`)
    if (!response.ok) throw new Error('Failed to fetch')
    return response.json()
  }
}
```

#### 3. Style Components

```css
/* frontend/src/styles/App.css */
.my-component {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 1.5rem;
}
```

## Database Schema

### Commands Table
```sql
CREATE TABLE commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_name TEXT UNIQUE NOT NULL,
    command_path TEXT NOT NULL,
    is_preset INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Settings Table
```sql
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
```

## Testing

### Backend Testing

```bash
# Install pytest
pip install pytest pytest-asyncio

# Run tests
pytest backend/tests/
```

Example test:
```python
# backend/tests/test_commands.py
import pytest
from app.models.repository import CommandRepository

def test_create_command():
    cmd_id = CommandRepository.create("test cmd", "/path/to/app")
    assert cmd_id > 0
    
    cmd = CommandRepository.get_by_name("test cmd")
    assert cmd is not None
    assert cmd["command_path"] == "/path/to/app"
```

### Frontend Testing

```bash
# Install testing library
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test
```

## Debugging

### Backend Debugging

1. **Enable Debug Logging:**
```python
# backend/app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Use FastAPI's Interactive Docs:**
Visit http://localhost:8000/docs

3. **Print Statements:**
```python
print(f"Debug: {variable}")
```

### Frontend Debugging

1. **Browser DevTools:**
   - Console: `console.log(data)`
   - Network tab: Monitor API calls
   - React DevTools: Inspect component state

2. **Error Boundaries:**
```jsx
class ErrorBoundary extends React.Component {
  componentDidCatch(error, info) {
    console.error('Error:', error, info)
  }
}
```

## Performance Optimization

### Backend
- Use async/await for I/O operations
- Cache frequently accessed data
- Index database columns
- Limit WebSocket message frequency

### Frontend
- Memoize expensive computations
- Lazy load components
- Debounce user inputs
- Optimize re-renders with React.memo

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions small and focused

### JavaScript (Frontend)
- Use ES6+ features
- Prefer functional components
- Use meaningful variable names
- Comment complex logic

## Common Tasks

### Add a New Preset Command

```python
# backend/app/main.py
PRESET_COMMANDS = {
    # ... existing commands ...
    "open myapp": "C:\\Path\\To\\MyApp.exe"
}
```

### Change Default Voice

```python
# backend/app/main.py
def seed_default_settings():
    SettingsRepository.set("voice", "female")  # Change to female
```

### Customize UI Theme

```css
/* frontend/src/styles/index.css */
:root {
  --primary-color: #00ff00;  /* Change primary color */
  --dark-bg: #000000;        /* Change background */
}
```

## Deployment

### Build Frontend

```bash
npm run build
# Output: dist/
```

### Package Backend

```bash
pip install pyinstaller
pyinstaller --onefile backend/app/main.py
```

### Environment Variables

```bash
# .env file
DATABASE_PATH=./echo.db
API_HOST=127.0.0.1
API_PORT=8000
FRONTEND_PORT=5173
```

## Contributing Guidelines

1. **Fork** the repository
2. **Create** a feature branch
3. **Write** tests for new features
4. **Update** documentation
5. **Submit** a pull request

### Commit Messages

- `feat: Add new feature`
- `fix: Fix bug in component`
- `docs: Update README`
- `refactor: Improve code structure`
- `test: Add tests for X`

## Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Vite Docs:** https://vitejs.dev/
- **SQLite Docs:** https://www.sqlite.org/docs.html
- **SpeechRecognition:** https://github.com/Uberi/speech_recognition
- **pyttsx3:** https://pyttsx3.readthedocs.io/

## Getting Help

- Read the error messages carefully
- Check the browser console for frontend issues
- Check the backend logs for API issues
- Use the API docs: http://localhost:8000/docs
- Search existing GitHub issues
- Create a new issue with reproduction steps

Happy developing! 🚀
