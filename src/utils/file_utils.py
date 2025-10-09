"""
File system utilities
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional

def find_directories_with_pattern(root_dir: str, pattern: str, max_depth: int = 3) -> List[str]:
    """
    Find directories containing files matching a pattern
    
    Args:
        root_dir: Root directory to search from
        pattern: File pattern to search for (e.g., "*.code-workspace")
        max_depth: Maximum search depth
        
    Returns:
        List of directory paths containing matching files
    """
    matching_dirs = []
    root_path = Path(root_dir)
    
    if not root_path.exists():
        return matching_dirs
    
    try:
        for path in root_path.rglob(pattern):
            if path.is_file():
                parent_dir = str(path.parent)
                if parent_dir not in matching_dirs:
                    # Check depth
                    relative_path = path.relative_to(root_path)
                    if len(relative_path.parts) <= max_depth:
                        matching_dirs.append(parent_dir)
    
    except PermissionError:
        pass
    except Exception as e:
        print(f"Error searching {root_dir}: {e}")
    
    return sorted(matching_dirs)

def get_directory_size(directory: str) -> int:
    """
    Get total size of directory in bytes
    
    Args:
        directory: Directory path
        
    Returns:
        Size in bytes
    """
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass
    except (OSError, PermissionError):
        pass
    
    return total_size

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def ensure_directory(directory: str) -> bool:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Directory path
        
    Returns:
        True if directory exists or was created successfully
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return False

def is_directory_writable(directory: str) -> bool:
    """
    Check if directory is writable
    
    Args:
        directory: Directory path
        
    Returns:
        True if writable, False otherwise
    """
    try:
        return os.access(directory, os.W_OK)
    except Exception:
        return False

def safe_copy_file(source: str, destination: str) -> bool:
    """
    Safely copy a file with error handling
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure destination directory exists
        dest_dir = os.path.dirname(destination)
        if dest_dir and not ensure_directory(dest_dir):
            return False
        
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"Error copying file {source} to {destination}: {e}")
        return False

def get_common_path_prefix(paths: List[str]) -> str:
    """
    Get common path prefix from a list of paths
    
    Args:
        paths: List of file/directory paths
        
    Returns:
        Common prefix path
    """
    if not paths:
        return ""
    
    if len(paths) == 1:
        return os.path.dirname(paths[0])
    
    try:
        return os.path.commonpath(paths)
    except ValueError:
        # No common path
        return ""

def normalize_path(path: str) -> str:
    """
    Normalize a file path
    
    Args:
        path: File or directory path
        
    Returns:
        Normalized path
    """
    return os.path.normpath(os.path.expanduser(path))

def relative_to_home(path: str) -> str:
    """
    Convert absolute path to path relative to home directory if possible
    
    Args:
        path: Absolute path
        
    Returns:
        Path relative to home or original path if not under home
    """
    try:
        home_path = Path.home()
        path_obj = Path(path)
        
        if path_obj.is_relative_to(home_path):
            relative = path_obj.relative_to(home_path)
            return f"~/{relative}"
        else:
            return path
    except Exception:
        return path