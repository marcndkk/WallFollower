#!/bin/sh
iw wlan0 set type ibss
ip link set wlan0 up
ip address add 192.168.99.11/24 broadcast + dev wlan0
iw wlan0 ibss join pibot 2432
