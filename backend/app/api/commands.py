from fastapi import APIRouter, HTTPException
from typing import List
from ..models.schemas import Command, CommandCreate, CommandUpdate
from ..models.repository import CommandRepository

router = APIRouter(prefix="/commands", tags=["commands"])

@router.get("/", response_model=List[Command])
async def get_commands():
    commands = CommandRepository.get_all()
    return commands

@router.post("/", response_model=dict)
async def create_command(command: CommandCreate):
    existing = CommandRepository.get_by_name(command.command_name)
    if existing:
        raise HTTPException(status_code=400, detail="Command already exists")
    
    command_id = CommandRepository.create(command.command_name, command.command_path)
    return {"id": command_id, "message": "Command created successfully"}

@router.put("/{command_name}", response_model=dict)
async def update_command(command_name: str, command: CommandUpdate):
    if command.command_path is None:
        raise HTTPException(status_code=400, detail="command_path is required")
    
    success = CommandRepository.update(command_name, command.command_path)
    if not success:
        raise HTTPException(status_code=404, detail="Command not found")
    
    return {"message": "Command updated successfully"}

@router.delete("/{command_name}", response_model=dict)
async def delete_command(command_name: str):
    success = CommandRepository.delete(command_name)
    if not success:
        raise HTTPException(status_code=404, detail="Command not found or is a preset command")
    
    return {"message": "Command deleted successfully"}
