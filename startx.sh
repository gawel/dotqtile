#!/bin/bash

fbsetbg -f /home/gawel/.backgrounds/nose_grind.jpg &
xscreensaver -nosplash &
xfce4-power-manager &
xfce4-volumed &
nm-applet &

dir=$(dirname $0)
config=$dir/config.py
qtile=$dir/venv/bin/qtile

#export PYTHONTRACEMALLOC=1

exec $qtile -c $config


