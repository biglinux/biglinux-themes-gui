#!/bin/bash

OIFS=$IFS
IFS=$'\n'

folder="/usr/share/biglinux/themes"



case "$1" in

    --apply)
	#Confere se o arquivo, diretório, link, ou arquivo especial NÃO existe
    if [ -e "$folder/$2" ]; then
        cp -Rf $folder/$2/. "$HOME"
        else
        echo "Theme not found."
    fi
    exit
    ;;

    --list)
	for i  in  $(ls $folder); do
        echo "$i"
    done
	exit
    ;;

    *)
	echo " Usage:
	--list
	--apply name-of-theme"
	exit
    ;;

esac



IFS=$OIFS

