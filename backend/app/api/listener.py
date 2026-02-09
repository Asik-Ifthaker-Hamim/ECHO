from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.listener import listener_service
import json

router = APIRouter(prefix="/listener", tags=["listener"])

@router.post("/start", response_model=dict)
async def start_listening():
    listener_service.start_listening()
    return {"message": "Listening started", "is_listening": True}

@router.post("/stop", response_model=dict)
async def stop_listening():
    listener_service.stop_listening()
    return {"message": "Listening stopped", "is_listening": False}

@router.get("/status", response_model=dict)
async def get_status():
    return {
        "is_listening": listener_service.is_running,
        "is_active": listener_service.listening_active
    }

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    async def send_status(status_data):
        try:
            await websocket.send_json(status_data)
        except:
            pass
    
    listener_service.set_status_callback(send_status)
    
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        pass
