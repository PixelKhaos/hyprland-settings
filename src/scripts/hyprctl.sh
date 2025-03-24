#!/bin/bash
#  _                          _   _ 
# | |__  _   _ _ __  _ __ ___| |_| |
# | '_ \| | | | '_ \| '__/ __| __| |
# | | | | |_| | |_) | | | (__| |_| |
# |_| |_|\__, | .__/|_|  \___|\__|_|
#        |___/|_|                   
# 
# Execute this file in the hyprland.conf with exec-always
sleep 3
script=$(readlink -f $0)
path=$(dirname $script)

if ! command -v hyprctl &> /dev/null; then
    echo ":: ERROR: hyprctl command not found"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo ":: ERROR: jq command not found"
    exit 1
fi

if [ ! -f $path/hyprctl.json ] ; then
    echo ":: ERROR: hyprctl.json not found"
    exit 1
fi

if ! jq empty $path/hyprctl.json 2>/dev/null; then
    echo ":: ERROR: hyprctl.json is not valid JSON"
    exit 1
fi

jq -c '.[]' $path/hyprctl.json | while read i; do
    _val() {
        echo $1 | jq -r '.value'
    }
    _key() {
        echo $1 | jq -r '.key'
    }
    key=$(_key $i)
    val=$(_val $i)
    echo ":: Execute: hyprctl keyword $key $val"
    if ! hyprctl keyword "$key" "$val"; then
        echo ":: WARNING: Failed to set $key to $val"
    fi
done
