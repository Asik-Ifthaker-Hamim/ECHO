@echo off
echo Starting ECHO Voice Assistant...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Check if backend dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing backend dependencies...
    pip install -r backend\requirements.txt
)

REM Check if node modules exist
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

echo.
echo Starting backend server...
start /B cmd /c "cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting frontend development server...
start /B cmd /c "npm run dev:vite"

echo.
echo ECHO is running!
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:5173
echo.
echo Press Ctrl+C to stop all servers...

pause
