from fastapi import APIRouter
from typing import Dict
from ..models.schemas import Setting
from ..models.repository import SettingsRepository
from ..services.speech import speech_service

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("/", response_model=Dict[str, str])
async def get_settings():
    return SettingsRepository.get_all()

@router.get("/{key}", response_model=Setting)
async def get_setting(key: str):
    value = SettingsRepository.get(key)
    if value is None:
        value = ""
    return {"key": key, "value": value}

@router.post("/{key}", response_model=dict)
async def set_setting(key: str, setting: Setting):
    SettingsRepository.set(key, setting.value)
    
    if key == "voice":
        speech_service.set_voice(setting.value)
    
    return {"message": "Setting updated successfully"}
