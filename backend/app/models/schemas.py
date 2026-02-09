from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommandBase(BaseModel):
    command_name: str
    command_path: str

class CommandCreate(CommandBase):
    pass

class CommandUpdate(BaseModel):
    command_path: Optional[str] = None

class Command(CommandBase):
    id: int
    is_preset: bool
    created_at: datetime

    class Config:
        from_attributes = True

class SettingBase(BaseModel):
    key: str
    value: str

class Setting(SettingBase):
    pass

class StatusUpdate(BaseModel):
    message: str
    color: str
    timestamp: datetime

class ListenStateUpdate(BaseModel):
    is_listening: bool
    is_active: bool
    message: str
