#!/bin/bash

iface=$(ip route | awk '/default/ {print $5; exit}')

if [ -z "$iface" ]; then
    echo "0 KB/s"
    exit
fi

if [ "$1" = "up" ]; then
    file="/sys/class/net/$iface/statistics/tx_bytes"
else
    file="/sys/class/net/$iface/statistics/rx_bytes"
fi

a=$(cat "$file")
sleep 1
b=$(cat "$file")

speed=$((b-a))

if [ "$speed" -ge 1048576 ]; then
    awk -v s="$speed" '{printf "%.1f MB/s", s/1048576}'
else
    awk -v s="$speed" '{printf "%.0f KB/s", s/1024}'
fi
