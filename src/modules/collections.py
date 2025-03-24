import gi
import os
import json
import shutil
from pathlib import Path

from gi.repository import Gtk, Adw

from .base import SettingsModule

class CollectionsModule(SettingsModule):
    def __init__(self, window):
        super().__init__(window)
        self.collections_dir = os.path.join(self.library.configFolder, "collections")
        self._ensure_collections_dir()
        
    def _ensure_collections_dir(self):
        """Ensure the collections directory exists"""
        Path(self.collections_dir).mkdir(parents=True, exist_ok=True)
        
    def get_collections(self):
        """Get list of available collections"""
        collections = []
        if os.path.exists(self.collections_dir):
            for file in os.listdir(self.collections_dir):
                if file.endswith('.json'):
                    name = file[:-5]
                    collections.append(name)
        return sorted(collections)
        
    def save_collection(self, name):
        """Save current settings as a new collection"""
        if not name:
            return False
            
        name = name.replace('/', '_').replace('\\', '_')
        filepath = os.path.join(self.collections_dir, f"{name}.json")
        
        # Copy current settings to collection
        try:
            shutil.copy2(
                os.path.join(self.library.configFolder, "hyprctl.json"),
                filepath
            )
            return True
        except Exception as e:
            print(f"Error saving collection: {e}")
            return False
            
    def load_collection(self, name):
        """Load settings from a collection"""
        filepath = os.path.join(self.collections_dir, f"{name}.json")
        if not os.path.exists(filepath):
            return False
            
        try:
            # Copy collection to current settings
            shutil.copy2(
                filepath,
                os.path.join(self.library.configFolder, "hyprctl.json")
            )
            
            self.library.executeHyprCtl()
            return True
        except Exception as e:
            print(f"Error loading collection: {e}")
            return False
            
    def delete_collection(self, name):
        """Delete a collection"""
        filepath = os.path.join(self.collections_dir, f"{name}.json")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except Exception as e:
                print(f"Error deleting collection: {e}")
        return False
        
    def create_collections_group(self):
        """Create the collections UI group"""
        group = self.create_group(
            "Collections",
            "Save and load different Hyprland configurations"
        )
        
        # Add New Collection button
        add_btn = Gtk.Button()
        add_btn.set_label("Save Current Settings as Collection")
        add_btn.set_halign(Gtk.Align.END)
        add_btn.connect("clicked", self._on_add_collection_clicked)
        add_btn.add_css_class("suggested-action")
        group.add(add_btn)
        
        # List existing collections
        collections = self.get_collections()
        for name in collections:
            row = self._create_collection_row(name)
            group.add(row)
            
        return group
        
    def _create_collection_row(self, name):
        """Create a row for a collection"""
        row = Adw.ActionRow()
        row.set_title(name)
        
        # Load button
        load_btn = Gtk.Button()
        load_btn.set_icon_name("folder-open-symbolic")
        load_btn.set_tooltip_text("Load this collection")
        load_btn.connect("clicked", self._on_load_collection_clicked, name)
        row.add_suffix(load_btn)
        
        # Delete button
        del_btn = Gtk.Button()
        del_btn.set_icon_name("edit-delete-symbolic")
        del_btn.set_tooltip_text("Delete this collection")
        del_btn.add_css_class("destructive-action")
        del_btn.connect("clicked", self._on_delete_collection_clicked, name)
        row.add_suffix(del_btn)
        
        return row
        
    def _on_add_collection_clicked(self, button):
        """Handle adding a new collection"""
        dialog = Adw.MessageDialog.new(
            self.window,
            "Save Collection",
            "Enter a name for your collection"
        )
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("save", "Save")
        dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
        
        entry = Gtk.Entry()
        entry.set_margin_top(10)
        entry.set_margin_bottom(10)
        entry.set_margin_start(10)
        entry.set_margin_end(10)
        dialog.set_extra_child(entry)
        
        dialog.connect("response", self._on_save_collection_response, entry)
        dialog.present()
        
    def _on_save_collection_response(self, dialog, response, entry):
        """Handle the save collection dialog response"""
        if response == "save":
            name = entry.get_text().strip()
            if name:
                if self.save_collection(name):
                    self.window.refresh_ui()
        dialog.destroy()
        
    def _on_load_collection_clicked(self, button, name):
        """Handle loading a collection"""
        dialog = Adw.MessageDialog.new(
            self.window,
            "Load Collection",
            f"Are you sure you want to load the collection '{name}'?\nThis will replace your current settings."
        )
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("load", "Load")
        dialog.set_response_appearance("load", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self._on_load_collection_response, name)
        dialog.present()
        
    def _on_load_collection_response(self, dialog, response, name):
        """Handle the load collection dialog response"""
        if response == "load":
            if self.load_collection(name):
                self.window.refresh_ui()
        dialog.destroy()
        
    def _on_delete_collection_clicked(self, button, name):
        """Handle deleting a collection"""
        dialog = Adw.MessageDialog.new(
            self.window,
            "Delete Collection",
            f"Are you sure you want to delete the collection '{name}'?"
        )
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("delete", "Delete")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        
        dialog.connect("response", self._on_delete_collection_response, name)
        dialog.present()
        
    def _on_delete_collection_response(self, dialog, response, name):
        """Handle the delete collection dialog response"""
        if response == "delete":
            if self.delete_collection(name):
                self.window.refresh_ui()
        dialog.destroy()
