#!/bin/bash

if [[ "$XDG_CURRENT_DESKTOP" == "GNOME" ]]; then

big-theme-apps --apply $1

else

big-theme-apps --apply $1

fi
