"""
Keyboard Shortcuts and Hotkeys
Global hotkey support for quick workspace access
"""

import threading
import time
from typing import Optional, Callable

try:
    import pynput
    from pynput import keyboard
    HOTKEY_AVAILABLE = True
except ImportError:
    HOTKEY_AVAILABLE = False

class HotkeyManager:
    """Manages global hotkeys for the application"""
    
    def __init__(self, show_window_callback: Callable):
        self.show_window = show_window_callback
        self.listener = None
        self.hotkey_combinations = {
            # Default hotkey: Ctrl+Alt+V (V for VS Code)
            frozenset([keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('v')]): self.show_window,
            frozenset([keyboard.Key.ctrl_r, keyboard.Key.alt_r, keyboard.KeyCode.from_char('v')]): self.show_window,
        }
        self.pressed_keys = set()
    
    def start_hotkey_listener(self) -> bool:
        """Start listening for global hotkeys"""
        if not HOTKEY_AVAILABLE:
            print("Global hotkeys not available (pynput not installed)")
            return False
        
        try:
            self.listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            
            def start_listener():
                self.listener.start()
            
            threading.Thread(target=start_listener, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"Error starting hotkey listener: {e}")
            return False
    
    def stop_hotkey_listener(self):
        """Stop listening for global hotkeys"""
        if self.listener:
            self.listener.stop()
            self.listener = None
    
    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            self.pressed_keys.add(key)
            
            # Check if any hotkey combination is pressed
            for combination, callback in self.hotkey_combinations.items():
                if combination.issubset(self.pressed_keys):
                    callback()
                    break
                    
        except Exception as e:
            print(f"Error in key press handler: {e}")
    
    def _on_key_release(self, key):
        """Handle key release events"""
        try:
            self.pressed_keys.discard(key)
        except Exception:
            pass
    
    def add_hotkey(self, keys: list, callback: Callable) -> bool:
        """Add a new hotkey combination"""
        try:
            key_set = frozenset(keys)
            self.hotkey_combinations[key_set] = callback
            return True
        except Exception as e:
            print(f"Error adding hotkey: {e}")
            return False
    
    def remove_hotkey(self, keys: list) -> bool:
        """Remove a hotkey combination"""
        try:
            key_set = frozenset(keys)
            if key_set in self.hotkey_combinations:
                del self.hotkey_combinations[key_set]
                return True
            return False
        except Exception as e:
            print(f"Error removing hotkey: {e}")
            return False

class KeyboardShortcuts:
    """Application keyboard shortcuts"""
    
    @staticmethod
    def setup_window_shortcuts(window, callback_map):
        """Setup keyboard shortcuts for a window"""
        for shortcut, callback in callback_map.items():
            window.bind(shortcut, lambda e, cb=callback: cb())
    
    @staticmethod
    def get_default_shortcuts():
        """Get default keyboard shortcuts"""
        return {
            '<Control-r>': 'refresh',
            '<Control-f>': 'search_focus',
            '<Control-o>': 'open_workspace',
            '<Control-n>': 'new_window',
            '<Control-q>': 'quit',
            '<F5>': 'refresh',
            '<Escape>': 'clear_search',
            '<Return>': 'open_workspace',
            '<Double-Button-1>': 'open_workspace',
            '<Button-3>': 'context_menu'
        }