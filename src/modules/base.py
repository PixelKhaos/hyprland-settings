import gi
import os
from gi.repository import Gtk, Adw

class SettingsModule:
    """Base class for all settings modules"""
    def __init__(self, window):
        self.window = window
        self.library = window.library
        
    def create_group(self, title, description=None):
        """Create a preferences group with title and optional description"""
        group = Adw.PreferencesGroup()
        group.set_title(title)
        if description:
            group.set_description(description)
        return group
