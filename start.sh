#!/bin/bash

echo "Starting ECHO Voice Assistant..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Check if backend dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing backend dependencies..."
    pip install -r backend/requirements.txt
fi

# Check if node modules exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo ""
echo "Starting backend server..."
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
cd ..

echo "Waiting for backend to start..."
sleep 3

echo "Starting frontend development server..."
npm run dev:vite &
FRONTEND_PID=$!

echo ""
echo "ECHO is running!"
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all servers..."

# Wait for user interrupt
wait $BACKEND_PID $FRONTEND_PID
