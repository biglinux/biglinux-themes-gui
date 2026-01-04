#!/bin/bash

if [[ "$XDG_CURRENT_DESKTOP" == "GNOME" ]]; then

big-theme-plasma --apply $1

else

big-theme-plasma --apply $1

fi
