#!/bin/bash
echo start | socat tcp:192.168.99.11:8080 -
echo
read -p "Press any key to stop.." -n1 -s
echo
echo stop | socat tcp:192.168.99.11:8080 -
echo
