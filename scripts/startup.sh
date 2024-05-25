#!/usr/bin/env bash

function run {
	if ! pgrep -f $1; then
		$@ &
	fi
}

set_wall() {
	wallpaper_path() {
		cat "/home/$USER/.config/wall.txt" | tail -n -1
	}
	run feh --bg-fill "$(wallpaper_path)"
}

run picom --config ~/.config/qtile/picom.conf &
run nm-applet &
run dunst &
run greenclip daemon &
run /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
run kdeconnect-indicator &
set_wall
