# Information
Server Pi is reachable with LAN on IP `192.168.1.1` and over wlan using `192.168.2.1`  
Audio Sinks can be listed using `pactl list sinks`

# Setup
For the setup the Pi needs Internet Access via LAN.
Before doing anything update the pi:
```
sudo apt update
sudo apt upgrade
``` 
For the video an `video.mp4` should be placed in this directory.  
Also make sure that a logs folder exists as otherwise the script won't work

## Displays
### Dependencies
```
sudo apt install mesa-utils
```
### TFT Display
Follow instructions here: https://github.com/pi3g/tft-display-setup
After the installation run this:
```
sudo systemctl stop fbcp
sudo systemctl disable fbcp
```
Edit XServer config `sudo nano /usr/share/X11/xorg.conf.d/99-fbdev.conf`:
```
Section "Device"  
  Identifier "myfb"
  Driver "fbdev"
  Option "fbdev" "/dev/fb1"
EndSection
```
### External Display
Modify the following line in /boot/config.txt
```
hdmi_cvt=640 480 60 1 0 0 0
```
to
```
hdmi_cvt=1920 1080 60 1 0 0 0
```
### Disable Screen Blanking
Using `sudo raspi-config` navigate to Display and disable screen blanking

## Networking
### Installing iperf3
```
cd ~
wget https://downloads.es.net/pub/iperf/iperf-3.14.tar.gz
tar -xf iperf-3.14.tar.gz
rm iperf-3.14.tar.gz
cd iperf-3.14
./configure; sudo make; sudo make install
sudo ldconfig /usr/local/lib
```
### WiFi Country
```
sudo raspi-config
```
Setup WiFi under `System Options` -> `Wireless LAN` with SSID `EMV-Test-Server` and Passphrase `zbMuW2jb;c9h5D7p?` and reboot the pi.
### WiFi Reconnect
In `/etc/network/interfaces` insert this at the end:
```
allow-hotplug wlan0
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
```

## SSD
### Dependencies
```
sudo apt install sysbench
```

## Bluetooth
### Fix SAP Driver Error
`sudo nano /etc/systemd/system/bluetooth.target.wants/bluetooth.service`
change
```
ExecStart=/usr/libexec/bluetooth/bluetoothd
```
to
```
ExecStart=/usr/libexec/bluetooth/bluetoothd --noplugin=sap
```
Reload systemd:
```
sudo systemctl daemon-reload
```
Restart bluetooth service:
```
sudo service bluetooth restart
```
### Pairing
The pairing has to be done manually: 20:64:DE:84:11:2C
```
bluetoothctl power on
bluetoothctl agent on
bluetoothctl scan on
bluetoothctl pair <MAC>
bluetoothctl trust <MAC>
bluetoothctl connect <MAC>
```

# Setup Autostart
```
(crontab -l 2>/dev/null || true; echo "@reboot sleep 45 && cd $PWD && python $PWD/client.py >> $PWD/client.log 2>&1") | crontab -
```