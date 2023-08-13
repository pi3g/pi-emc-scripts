#!/bin/bash
cd "$(dirname "$0")"

echo "" > server.log
mkdir -p logs
echo "" > logs/iperf_lan.log
echo "" > logs/iperf_wlan.log
