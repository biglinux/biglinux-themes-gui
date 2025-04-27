"""
Internationalization module for BigLinux Themes GUI.
Handles translation setup and provides the gettext function.
"""

import gettext
import locale
import os

# Set up locale
locale.setlocale(locale.LC_ALL, "")


# Get the current directory for locating translation files
def _get_current_dir():
    return os.path.dirname(os.path.abspath(__file__))


# Set up gettext for translations
_localedir = os.path.join(_get_current_dir(), "locale")
_translation = gettext.translation("biglinux-themes-gui", _localedir, fallback=True)
_ = _translation.gettext


# Make the translation function available
def get_translation_function():
    """Return the translation function."""
    return _
