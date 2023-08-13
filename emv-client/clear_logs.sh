#!/bin/bash
cd "$(dirname "$0")"

echo "" > client.log
mkdir -p logs
echo "" > logs/audio.log
echo "" > logs/fileio.log
echo "" > logs/glxgears.log
echo "" > logs/iperf_lan.log
echo "" > logs/iperf_wlan.log
echo "" > logs/mplayer.log
