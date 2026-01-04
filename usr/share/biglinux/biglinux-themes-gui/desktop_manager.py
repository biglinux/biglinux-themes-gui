"""
Desktop manager module for BigLinux Themes GUI.
Handles desktop operations and provides desktop-related functionality.
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
from utils import (
    get_current_desktop,
    get_desktop_list,
    check_desktop_used,
    apply_desktop,
    get_current_dir,
)


class DesktopManager:
    """Manager for desktop operations."""

    def __init__(self):
        """Initialize the desktop manager."""
        self.current_desktop = get_current_desktop()
        self.desktop_list = get_desktop_list()
        self.selected_desktop = None
        self.desktop_changed_callbacks = []

    def get_current_desktop(self) -> str:
        """Get the currently active desktop configuration."""
        self.current_desktop = get_current_desktop()
        return self.current_desktop

    def get_desktop_list(self) -> List[str]:
        """Get the list of available desktop configurations."""
        return self.desktop_list

    def set_desktop(self, desktop_name: str, clean: str = "") -> None:
        """Set a desktop configuration as active."""
        apply_desktop(desktop_name, clean)
        self.current_desktop = desktop_name
        self._notify_desktop_changed()

    def is_desktop_used(self, desktop_name: str) -> bool:
        """Check if a desktop configuration has been used before."""
        return check_desktop_used(desktop_name)

    def _notify_desktop_changed(self) -> None:
        """Notify all registered callbacks about a desktop change."""
        for callback in self.desktop_changed_callbacks:
            callback(self.current_desktop)

    def get_desktop_image_path(self, desktop_name: str) -> str:
        """Get the path to a desktop configuration's preview image."""
        return os.path.join(get_current_dir(), "img", f"{desktop_name}.svg")

    def create_desktop_widget(self, desktop_name: str) -> Gtk.Box:
        """Create a widget for displaying a desktop configuration in the UI."""
        # Image dimensions - fixed size for the desktop images
        img_width = 40
        img_height = 28
        # Padding - exactly 5px on each side
        padding = 5

        # Create a fixed-size container
        outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Add CSS class for hover effect
        outer_box.add_css_class("clickable-item")

        # Set exact size of outer box (image + padding)
        outer_box.set_size_request(
            img_width + (padding * 2), img_height + (padding * 2)
        )

        # Fix the box size and prevent expansion
        outer_box.set_hexpand(False)
        outer_box.set_vexpand(False)

        # Center alignment
        outer_box.set_halign(Gtk.Align.CENTER)
        outer_box.set_valign(Gtk.Align.CENTER)

        # If this is the current desktop, add selected class
        if desktop_name == self.current_desktop:
            outer_box.add_css_class("selected-desktop")

        # Set pointer cursor
        cursor = Gdk.Cursor.new_from_name("pointer", None)
        outer_box.set_cursor(cursor)

        # Set tooltip
        display_name = desktop_name.replace("-", " ")
        tooltip = _("Click to switch to the {} desktop environment").format(
            display_name
        )
        outer_box.set_tooltip_text(tooltip)

        # Create inner container for the picture with exact padding
        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        inner_box.set_size_request(img_width, img_height)
        inner_box.set_halign(Gtk.Align.CENTER)
        inner_box.set_valign(Gtk.Align.CENTER)

        # Add padding to position the image inside the outer box
        inner_box.set_margin_start(padding)
        inner_box.set_margin_end(padding)
        inner_box.set_margin_top(padding)
        inner_box.set_margin_bottom(padding)

        # Load and create the image
        image_path = self.get_desktop_image_path(desktop_name)
        try:
            if image_path.lower().endswith(".svg"):
                picture = Gtk.Picture.new_for_filename(image_path)
                picture.set_size_request(img_width, img_height)
                picture.set_hexpand(True)
                picture.set_vexpand(True)
                picture.set_halign(Gtk.Align.CENTER)
                picture.set_valign(Gtk.Align.CENTER)
            else:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    image_path,
                    img_width,
                    img_height,
                    True,
                )
                picture = Gtk.Picture.new_for_pixbuf(pixbuf)
                picture.set_size_request(img_width, img_height)
                picture.set_keep_aspect_ratio(True)
                picture.set_halign(Gtk.Align.CENTER)
                picture.set_valign(Gtk.Align.CENTER)
                picture.set_hexpand(False)
                picture.set_vexpand(False)
        except GLib.Error as e:
            print(f"Error loading image {image_path}: {e}")
            picture = Gtk.Picture()
            picture.set_size_request(img_width, img_height)
            picture.set_halign(Gtk.Align.CENTER)
            picture.set_valign(Gtk.Align.CENTER)
            picture.set_hexpand(False)
            picture.set_vexpand(False)

        # Add picture to inner box, then add inner box to outer box
        inner_box.append(picture)
        outer_box.append(inner_box)

        return outer_box
