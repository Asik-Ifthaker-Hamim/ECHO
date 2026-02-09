import os
import subprocess
from typing import Optional, Tuple
from ..models.repository import CommandRepository

class CommandService:
    @staticmethod
    def execute_command(command: str) -> Tuple[bool, str, str]:
        if "find" in command:
            search_item = command.replace("find ", "")
            return CommandService.search_and_open(search_item)
        
        command_dict = CommandRepository.get_command_dict()
        
        if command in command_dict:
            path_or_command = command_dict[command]
            try:
                if isinstance(path_or_command, list):
                    subprocess.Popen(path_or_command)
                else:
                    subprocess.Popen(path_or_command, shell=True)
                
                app_name = command.replace("open ", "")
                return True, f"Opening: {app_name}", "green"
            except Exception as e:
                return False, f"Error: {str(e)}", "red"
        else:
            return False, "Command not recognized.", "red"
    
    @staticmethod
    def search_and_open(target_name: str) -> Tuple[bool, str, str]:
        found_paths = []
        
        search_root = "C:\\" if os.name == 'nt' else os.path.expanduser("~")
        
        try:
            for root_dir, dirs, files in os.walk(search_root):
                for folder in dirs:
                    if target_name.lower() in folder.lower():
                        found_paths.append(os.path.join(root_dir, folder))
                for file in files:
                    if target_name.lower() in file.lower():
                        found_paths.append(os.path.join(root_dir, file))
                
                if len(found_paths) > 0:
                    break
        except Exception as e:
            return False, f"Search error: {str(e)}", "red"
        
        if found_paths:
            target_path = found_paths[0]
            try:
                if os.name == 'nt':
                    subprocess.Popen(f'explorer "{target_path}"', shell=True)
                else:
                    subprocess.Popen(['xdg-open', target_path])
                return True, f"Opening: {target_path}", "green"
            except Exception as e:
                return False, f"Error opening file: {str(e)}", "red"
        else:
            return False, f"'{target_name}' not found.", "red"

command_service = CommandService()
