# window.py
#
# Copyright 2025 Unknown
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk

from .library.library import Library
from .modules.collections import CollectionsModule

@Gtk.Template(resource_path='/com/ml4w/hyprlandsettings/window.ui')
class HyprlandSettingsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'Ml4wHyprlandSettingsWindow'

    keywords_group = Gtk.Template.Child()
    novariables = Gtk.Template.Child()
    main_box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.library = Library()
        
        self.collections_module = CollectionsModule(self)
        
        self.collections_group = self.collections_module.create_collections_group()
        self.main_box.append(self.collections_group)

    def refresh_ui(self):
        """Refresh all UI elements to reflect current settings"""
        # TODO: Refresh other UI elements as they are added
        # For now, just refresh collections
        old_group = self.collections_group
        new_group = self.collections_module.create_collections_group()
        parent = old_group.get_parent()
        parent.remove(old_group)
        parent.append(new_group)
        self.collections_group = new_group
