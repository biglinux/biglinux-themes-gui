"""
Theme manager module for BigLinux Themes GUI.
Handles theme operations and provides theme-related functionality.
"""

from typing import List
import os
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
# Add Gdk to imports
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

# Import the translation function
from i18n import _
from utils import get_current_theme, get_theme_list, apply_theme, get_current_dir


class ThemeManager:
    """Manager for theme operations."""

    def __init__(self):
        """Initialize the theme manager."""
        self.current_theme = get_current_theme()
        self.theme_list = get_theme_list()
        self.theme_changed_callbacks = []

    def get_current_theme(self) -> str:
        """Get the currently active theme."""
        self.current_theme = get_current_theme()
        return self.current_theme

    def get_theme_list(self) -> List[str]:
        """Get the list of available themes."""
        return self.theme_list

    def set_theme(self, theme_name: str) -> None:
        """Set a theme as active."""
        apply_theme(theme_name)
        self.current_theme = theme_name
        self._notify_theme_changed()

    def _notify_theme_changed(self) -> None:
        """Notify all registered callbacks about a theme change."""
        for callback in self.theme_changed_callbacks:
            callback(self.current_theme)

    def get_theme_image_path(self, theme_name: str) -> str:
        """Get the path to a theme's preview image."""
        return os.path.join(get_current_dir(), "img", f"{theme_name}.png")

    def create_theme_widget(self, theme_name: str) -> Gtk.Box:
        """Create a widget for displaying a theme in the UI."""
        # Create main container
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_start(8)
        box.set_margin_end(8)
        box.set_margin_top(0)
        box.set_margin_bottom(0)
        box.set_hexpand(True)
        box.set_vexpand(True)
        box.set_homogeneous(False)

        # Create an outer box to handle the hover effect without affecting content size
        outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        outer_box.set_hexpand(True)
        outer_box.set_vexpand(True)
        outer_box.add_css_class("clickable-item")  # Custom CSS class for hover effects
        outer_box.append(box)

        # Set cursor to pointer using GTK4 method
        cursor = Gdk.Cursor.new_from_name("pointer", None)
        outer_box.set_cursor(cursor)

        # Create tooltip
        display_name = theme_name.replace("-", " ")
        tooltip = _("Click to apply the {} theme").format(display_name)
        box.set_tooltip_text(tooltip)

        # Create image widget
        image_path = self.get_theme_image_path(theme_name)
        try:
            # Don't set fixed scale, let it adapt to container
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)

            # Create picture that can scale with the container
            picture = Gtk.Picture.new_for_pixbuf(pixbuf)
            picture.set_keep_aspect_ratio(True)
            picture.set_hexpand(True)
            picture.set_vexpand(True)
            picture.set_can_shrink(True)
        except GLib.Error:
            # Fallback if image cannot be loaded
            picture = Gtk.Picture()
            picture.set_hexpand(True)
            picture.set_vexpand(True)

        # Create label for theme name
        label = Gtk.Label(label=theme_name.replace("-", " "))
        label.set_margin_top(0)
        label.set_ellipsize(True)
        label.set_max_width_chars(25)

        # Add widgets to container
        box.append(picture)
        box.append(label)

        return box
