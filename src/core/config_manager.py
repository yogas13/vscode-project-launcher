"""
Configuration Manager
Handles application settings and persistent storage
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class AppConfig:
    """Application configuration settings"""
    scan_directories: List[str]
    favorites: List[str]
    recent_workspaces: List[str]
    window_geometry: Dict[str, int]
    auto_scan: bool
    max_recent: int
    theme: str
    show_folder_count: bool
    recursive_scan: bool
    
    @classmethod
    def default(cls):
        """Create default configuration"""
        home_dir = str(Path.home())
        dev_dir = os.path.join(home_dir, "dev")
        projects_dir = os.path.join(home_dir, "projects")
        
        # Default scan directories (common development folder locations)
        default_dirs = [
            dev_dir if os.path.exists(dev_dir) else home_dir,
            projects_dir if os.path.exists(projects_dir) else None,
            os.path.join(home_dir, "Documents"),
            os.path.join(home_dir, "Development"),
        ]
        
        # Filter out None values and non-existent directories
        scan_dirs = [d for d in default_dirs if d and os.path.exists(d)]
        if not scan_dirs:
            scan_dirs = [home_dir]
        
        return cls(
            scan_directories=scan_dirs,
            favorites=[],
            recent_workspaces=[],
            window_geometry={"width": 800, "height": 600, "x": 100, "y": 100},
            auto_scan=True,
            max_recent=10,
            theme="default",
            show_folder_count=True,
            recursive_scan=True
        )

class ConfigManager:
    """Manages application configuration and settings"""
    
    def __init__(self):
        self.app_name = "vscode-launcher"
        self.config_dir = Path.home() / ".config" / self.app_name
        self.config_file = self.config_dir / "config.json"
        self._config = None
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self.load_config()
    
    def load_config(self) -> AppConfig:
        """Load configuration from file or create default"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Merge with defaults to handle missing keys
                default_config = AppConfig.default()
                default_dict = asdict(default_config)
                
                # Update defaults with loaded values
                for key, value in config_data.items():
                    if key in default_dict:
                        default_dict[key] = value
                
                self._config = AppConfig(**default_dict)
            else:
                self._config = AppConfig.default()
                self.save_config()
                
        except Exception as e:
            print(f"Error loading config: {e}")
            self._config = AppConfig.default()
            
        return self._config
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            config_dict = asdict(self._config)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    @property
    def config(self) -> AppConfig:
        """Get current configuration"""
        return self._config
    
    def update_config(self, **kwargs) -> bool:
        """Update configuration with new values"""
        try:
            config_dict = asdict(self._config)
            config_dict.update(kwargs)
            self._config = AppConfig(**config_dict)
            return self.save_config()
        except Exception as e:
            print(f"Error updating config: {e}")
            return False
    
    def add_scan_directory(self, directory: str) -> bool:
        """Add a directory to the scan list"""
        if os.path.exists(directory) and directory not in self._config.scan_directories:
            self._config.scan_directories.append(directory)
            return self.save_config()
        return False
    
    def remove_scan_directory(self, directory: str) -> bool:
        """Remove a directory from the scan list"""
        if directory in self._config.scan_directories:
            self._config.scan_directories.remove(directory)
            return self.save_config()
        return False
    
    def add_favorite(self, workspace_path: str) -> bool:
        """Add a workspace to favorites"""
        if workspace_path not in self._config.favorites:
            self._config.favorites.append(workspace_path)
            return self.save_config()
        return False
    
    def remove_favorite(self, workspace_path: str) -> bool:
        """Remove a workspace from favorites"""
        if workspace_path in self._config.favorites:
            self._config.favorites.remove(workspace_path)
            return self.save_config()
        return False
    
    def is_favorite(self, workspace_path: str) -> bool:
        """Check if a workspace is in favorites"""
        return workspace_path in self._config.favorites
    
    def add_recent_workspace(self, workspace_path: str) -> bool:
        """Add a workspace to recent list"""
        # Remove if already exists to move to front
        if workspace_path in self._config.recent_workspaces:
            self._config.recent_workspaces.remove(workspace_path)
        
        # Add to front
        self._config.recent_workspaces.insert(0, workspace_path)
        
        # Limit to max_recent items
        self._config.recent_workspaces = self._config.recent_workspaces[:self._config.max_recent]
        
        return self.save_config()
    
    def clear_recent_workspaces(self) -> bool:
        """Clear the recent workspaces list"""
        self._config.recent_workspaces.clear()
        return self.save_config()
    
    def update_window_geometry(self, width: int, height: int, x: int, y: int) -> bool:
        """Update window geometry settings"""
        self._config.window_geometry = {
            "width": width,
            "height": height,
            "x": x,
            "y": y
        }
        return self.save_config()
    
    def export_config(self, export_path: str) -> bool:
        """Export configuration to a file"""
        try:
            shutil.copy2(self.config_file, export_path)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Import configuration from a file"""
        try:
            # Validate the config file first
            with open(import_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Backup current config
            backup_path = self.config_file.with_suffix('.json.backup')
            if self.config_file.exists():
                shutil.copy2(self.config_file, backup_path)
            
            # Copy new config
            shutil.copy2(import_path, self.config_file)
            
            # Reload configuration
            self.load_config()
            return True
            
        except Exception as e:
            print(f"Error importing config: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values"""
        try:
            self._config = AppConfig.default()
            return self.save_config()
        except Exception as e:
            print(f"Error resetting config: {e}")
            return False