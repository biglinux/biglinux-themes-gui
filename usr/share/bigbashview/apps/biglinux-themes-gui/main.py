#!/usr/bin/env python3.13
"""
BigLinux Themes GUI
A GTK4 application for managing BigLinux themes and desktop configurations.
"""

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio

# Import the translation function
from i18n import _
from window import ThemesWindow


class BigLinuxThemesApplication(Adw.Application):
    """Main application class for BigLinux Themes GUI."""

    def __init__(self):
        """Initialize the application."""
        super().__init__(
            application_id="org.biglinux.themes", flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        """Create and show the main window when the application is activated."""
        # Use system color scheme preference with error handling
        window = ThemesWindow(application=app)
        window.present()


def main():
    """Start the application."""
    app = BigLinuxThemesApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
