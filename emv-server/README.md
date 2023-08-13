# Information
To view the Client Pi's DHCP Leases use `cat /var/lib/misc/dnsmasq.leases` there should be two entries in the file.  
After pressing exit on the Internal Display it may take up to 10 Seconds for everything to close.

# Setup
For the setup the Pi needs WiFi access via a USB to LAN Adapter since the setup changes eth0 and wlan0 behavior.
Before doing anything update the pi:
```
sudo apt update
sudo apt upgrade
```
Make sure that a logs folder exists as otherwise the script won't work

## Display Setup
Follow instructions here: https://github.com/pi3g/tft-display-setup
### Install PySimpleGUI for Status Display
```
pip install PySimpleGUI
```
### Disable Screen Blanking
Using `sudo raspi-config` navigate to Display and disable screen blanking

## Networking Setup
Install hostapd and dnsmasq for hosting a WiFi access point, a DHCP and DNS server and iperf for bandwith testing.
```
sudo apt install hostapd dnsmasq
sudo service dnsmasq stop
sudo service hostapd stop
```
### Installing iperf3
Current repository version is too old so we need to build it manually
```
cd ~
wget https://downloads.es.net/pub/iperf/iperf-3.14.tar.gz
tar -xf iperf-3.14.tar.gz
rm iperf-3.14.tar.gz
cd iperf-3.14
./configure; make; sudo make install
sudo ldconfig /usr/local/lib
```
### WiFi Country
```
sudo raspi-config
```
Choose `Localisation Options` and then `Change Wi-Fi Country` and reboot the Pi afterwards.
### dhcpcd Config
```
sudo nano /etc/dhcpcd.conf
```
At the end insert the following
```
interface eth0
    static ip_address=192.168.1.1/24

interface wlan0
    static ip_address=192.168.2.1/24
```
Restart dhcpcd
```
sudo service dhcpcd restart
```
### dnsmasq Config
```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf
```
At the end insert the following
```
interface=eth0
    dhcp-range=192.168.1.2,192.168.1.20,255.255.255.0,48h

interface=wlan0
    dhcp-range=192.168.2.2,192.168.2.20,255.255.255.0,48h
```
### hostapd Config
```
sudo nano /etc/hostapd/hostapd.conf
```
At the end instert the following
```
interface=wlan0

# 2.4GHz Mode
hw_mode=g
channel=7

# 5GHz Mode
# hw_mode=a
# channel=40

macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=EMV-Test-Server
wpa_passphrase=zbMuW2jb;c9h5D7p?
```
Link the file as the default
```
sudo nano /etc/default/hostapd
```
Look for the line `#DAEMON_CONF=""` and replace it with
```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```
### Restart Services
```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo service hostapd start
sudo service dnsmasq start
```

# Setup Autostart
```
(crontab -l 2>/dev/null || true; echo "@reboot sleep 15 && sudo service hostapd restart && export DISPLAY=:0 && cd $PWD && python $PWD/server.py >> $PWD/server.log 2>&1") | crontab -
```