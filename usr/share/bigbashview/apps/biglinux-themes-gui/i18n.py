"""
Internationalization module for BigLinux Themes GUI.
Handles translation setup and provides the gettext function.
"""

import gettext
# Configure the translation repo/name
gettext.textdomain("biglinux-themes-gui")
# Export _ directly as the translation function
_ = gettext.gettext
