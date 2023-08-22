#!/bin/bash
picom --blur-method dual_kawase &
./.fehbg &

xautolock -locker "bash ~/turnoff.sh" &
lxsession &
xrandr --output HDMI-A-0 --right-of HDMI-A-1 &

