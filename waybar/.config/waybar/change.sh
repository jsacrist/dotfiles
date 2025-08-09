#!/bin/sh

DIR=$1

if [ ! -e "${DIR}"/style.css ]; then
	echo "file not found: ${DIR}/style.css"
	exit 1
fi

if [ ! -e "${DIR}"/config.jsonc ]; then
	echo "file not found: ${DIR}/config.jsonc"
	exit 1
fi

rm style.css
ln -s "${DIR}"/style.css style.css

rm config.jsonc
ln -s "${DIR}"/config.jsonc

# pkill waybar && hyprctl dispatch exec waybar
