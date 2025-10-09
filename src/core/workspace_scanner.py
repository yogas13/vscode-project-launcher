"""
Workspace Scanner
Handles scanning directories for VS Code workspace files and extracting metadata
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkspaceInfo:
    """Information about a VS Code workspace"""
    name: str
    path: str
    full_path: str
    folder_count: int
    folders: List[str]
    last_modified: datetime
    size: int
    
    def __str__(self):
        return f"{self.name} ({self.folder_count} folders)"

class WorkspaceScanner:
    """Scans directories for VS Code workspace files"""
    
    def __init__(self):
        self.workspace_extensions = ['.code-workspace']
        self._cache = {}
        
    def scan_directory(self, directory: str, recursive: bool = True) -> List[WorkspaceInfo]:
        """
        Scan a directory for workspace files
        
        Args:
            directory: Path to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of WorkspaceInfo objects
        """
        workspaces = []
        directory_path = Path(directory)
        
        if not directory_path.exists() or not directory_path.is_dir():
            return workspaces
            
        try:
            if recursive:
                pattern = "**/*.code-workspace"
                workspace_files = directory_path.glob(pattern)
            else:
                pattern = "*.code-workspace"
                workspace_files = directory_path.glob(pattern)
                
            for workspace_file in workspace_files:
                workspace_info = self._parse_workspace_file(workspace_file)
                if workspace_info:
                    workspaces.append(workspace_info)
                    
        except PermissionError:
            print(f"Permission denied accessing: {directory}")
        except Exception as e:
            print(f"Error scanning {directory}: {e}")
            
        return workspaces
    
    def scan_multiple_directories(self, directories: List[str], recursive: bool = True) -> List[WorkspaceInfo]:
        """
        Scan multiple directories for workspace files
        
        Args:
            directories: List of directory paths to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of WorkspaceInfo objects from all directories
        """
        all_workspaces = []
        seen_paths = set()
        
        for directory in directories:
            workspaces = self.scan_directory(directory, recursive)
            for workspace in workspaces:
                # Avoid duplicates
                if workspace.full_path not in seen_paths:
                    all_workspaces.append(workspace)
                    seen_paths.add(workspace.full_path)
                    
        return sorted(all_workspaces, key=lambda w: w.name.lower())
    
    def _parse_workspace_file(self, file_path: Path) -> Optional[WorkspaceInfo]:
        """
        Parse a workspace file and extract information
        
        Args:
            file_path: Path to the workspace file
            
        Returns:
            WorkspaceInfo object or None if parsing failed
        """
        try:
            # Check if file is cached and hasn't been modified
            stat = file_path.stat()
            cache_key = str(file_path)
            
            if (cache_key in self._cache and 
                self._cache[cache_key]['mtime'] == stat.st_mtime):
                return self._cache[cache_key]['workspace_info']
            
            # Read and parse the workspace file
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    workspace_data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Invalid JSON in workspace file: {file_path}")
                    return None
            
            # Extract folder information
            folders = []
            folder_count = 0
            
            if 'folders' in workspace_data:
                for folder in workspace_data['folders']:
                    if 'path' in folder:
                        folder_path = folder['path']
                        # Handle relative paths
                        if not os.path.isabs(folder_path):
                            folder_path = os.path.join(file_path.parent, folder_path)
                        folders.append(folder_path)
                        folder_count += 1
            
            # Generate workspace name
            workspace_name = self._generate_workspace_name(file_path, folders)
            
            # Create WorkspaceInfo object
            workspace_info = WorkspaceInfo(
                name=workspace_name,
                path=str(file_path.parent),
                full_path=str(file_path),
                folder_count=folder_count,
                folders=folders,
                last_modified=datetime.fromtimestamp(stat.st_mtime),
                size=stat.st_size
            )
            
            # Cache the result
            self._cache[cache_key] = {
                'mtime': stat.st_mtime,
                'workspace_info': workspace_info
            }
            
            return workspace_info
            
        except Exception as e:
            print(f"Error parsing workspace file {file_path}: {e}")
            return None
    
    def _generate_workspace_name(self, file_path: Path, folders: List[str]) -> str:
        """
        Generate a display name for the workspace
        
        Args:
            file_path: Path to the workspace file
            folders: List of folder paths in the workspace
            
        Returns:
            Human-readable workspace name
        """
        # Start with the filename without extension
        base_name = file_path.stem
        
        # Clean up the name (remove common prefixes/suffixes)
        base_name = re.sub(r'\.code-workspace$', '', base_name)
        
        # If the workspace name is generic, try to use folder information
        if base_name.lower() in ['workspace', 'main', 'default'] and folders:
            # Use the name of the first folder
            first_folder = Path(folders[0])
            base_name = first_folder.name
        
        # Capitalize and clean up the name
        base_name = base_name.replace('_', ' ').replace('-', ' ')
        base_name = ' '.join(word.capitalize() for word in base_name.split())
        
        return base_name
    
    def clear_cache(self):
        """Clear the workspace file cache"""
        self._cache.clear()
    
    def get_workspace_by_path(self, workspace_path: str) -> Optional[WorkspaceInfo]:
        """
        Get workspace information for a specific file path
        
        Args:
            workspace_path: Full path to the workspace file
            
        Returns:
            WorkspaceInfo object or None if not found
        """
        file_path = Path(workspace_path)
        if file_path.exists() and file_path.suffix == '.code-workspace':
            return self._parse_workspace_file(file_path)
        return None