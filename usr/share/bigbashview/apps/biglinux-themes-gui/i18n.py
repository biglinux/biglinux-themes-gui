"""
Internationalization module for BigLinux Themes GUI.
Handles translation setup and provides the gettext function.
"""

import gettext

gettext.textdomain("biglinux-themes-gui")
_ = gettext.gettext
