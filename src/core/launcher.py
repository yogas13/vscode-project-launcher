"""
VS Code Launcher
Handles launching VS Code with workspace files
"""

import os
import subprocess
import shutil
from typing import Optional
from pathlib import Path

class VSCodeLauncher:
    """Handles launching VS Code with workspace files"""
    
    def __init__(self):
        self.vscode_commands = ['code', 'code-insiders', 'codium', 'vscodium']
        self._vscode_path = None
        self._find_vscode()
    
    def _find_vscode(self) -> Optional[str]:
        """Find VS Code executable"""
        for cmd in self.vscode_commands:
            path = shutil.which(cmd)
            if path:
                self._vscode_path = path
                return path
        return None
    
    @property
    def is_available(self) -> bool:
        """Check if VS Code is available"""
        return self._vscode_path is not None
    
    @property
    def vscode_path(self) -> Optional[str]:
        """Get the VS Code executable path"""
        return self._vscode_path
    
    def launch_workspace(self, workspace_path: str, new_window: bool = False) -> bool:
        """
        Launch VS Code with a workspace file
        
        Args:
            workspace_path: Path to the .code-workspace file
            new_window: Whether to open in a new window
            
        Returns:
            True if launch was successful, False otherwise
        """
        if not self.is_available:
            print("VS Code is not installed or not found in PATH")
            return False
        
        if not os.path.exists(workspace_path):
            print(f"Workspace file not found: {workspace_path}")
            return False
        
        try:
            cmd = [self._vscode_path]
            
            if new_window:
                cmd.append('--new-window')
            
            cmd.append(workspace_path)
            
            # Launch VS Code in the background
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            return True
            
        except Exception as e:
            print(f"Error launching VS Code: {e}")
            return False
    
    def launch_folder(self, folder_path: str, new_window: bool = False) -> bool:
        """
        Launch VS Code with a folder
        
        Args:
            folder_path: Path to the folder to open
            new_window: Whether to open in a new window
            
        Returns:
            True if launch was successful, False otherwise
        """
        if not self.is_available:
            print("VS Code is not installed or not found in PATH")
            return False
        
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return False
        
        try:
            cmd = [self._vscode_path]
            
            if new_window:
                cmd.append('--new-window')
            
            cmd.append(folder_path)
            
            # Launch VS Code in the background
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            return True
            
        except Exception as e:
            print(f"Error launching VS Code: {e}")
            return False
    
    def open_settings(self, workspace_path: Optional[str] = None) -> bool:
        """
        Open VS Code settings
        
        Args:
            workspace_path: Optional workspace to open settings for
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available:
            return False
        
        try:
            cmd = [self._vscode_path, '--command', 'workbench.action.openSettings']
            
            if workspace_path and os.path.exists(workspace_path):
                cmd.append(workspace_path)
            
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            return True
            
        except Exception as e:
            print(f"Error opening VS Code settings: {e}")
            return False
    
    def get_version(self) -> Optional[str]:
        """
        Get VS Code version
        
        Returns:
            Version string or None if not available
        """
        if not self.is_available:
            return None
        
        try:
            result = subprocess.run(
                [self._vscode_path, '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    return lines[0]  # First line contains version
            
        except Exception as e:
            print(f"Error getting VS Code version: {e}")
        
        return None
    
    def create_workspace_file(self, workspace_path: str, folders: list, 
                            settings: dict = None, extensions: dict = None) -> bool:
        """
        Create a new VS Code workspace file
        
        Args:
            workspace_path: Path where to create the workspace file
            folders: List of folder paths to include
            settings: Optional workspace settings
            extensions: Optional workspace extensions
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import json
            
            workspace_data = {
                "folders": [{"path": folder} for folder in folders]
            }
            
            if settings:
                workspace_data["settings"] = settings
            
            if extensions:
                workspace_data["extensions"] = extensions
            
            with open(workspace_path, 'w', encoding='utf-8') as f:
                json.dump(workspace_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error creating workspace file: {e}")
            return False