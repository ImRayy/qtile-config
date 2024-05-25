#!/usr/bin/env bash

volume_step=2
max_volume=100
notification_timeout=1000

function get_volume {
	pamixer --get-volume
}

function get_mute {
	[[ $(get_volume) == 0 ]] && echo "yes" || echo "no"
}

get_mute

function get_volume_icon {
	volume=$(get_volume)
	mute=$(get_mute)
	if [[ "$mute" == "yes" ]]; then
		echo " "
	elif [[ "$volume" -lt 50 ]]; then
		echo ""
	elif [[ "$volume" -lt 80 ]]; then
		echo " "
	else
		echo ""
	fi
}

# get_volume_icon

function show_volume_notif {
	volume=$(get_volume)
	volume_icon=$(get_volume_icon)
	notify-send -t $notification_timeout -h string:x-dunst-stack-tag:volume_notif -h int:value:$volume "$volume_icon $volume%"
}

case $1 in
volume_up)
	volume=$(get_volume)
	if [[ "$volume" -lt $max_volume ]]; then
		pamixer -i $volume_step
	fi
	show_volume_notif
	;;
volume_down)
	pamixer -d $volume_step
	show_volume_notif
	;;
volume_mute)
	pamixer -t
	show_volume_notif
	;;
esac
