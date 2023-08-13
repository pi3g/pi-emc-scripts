from modules.IPerfClient import IPerfClient
from modules.GLXGears import GLXGears
from modules.MPlayer import MPlayer
from modules.Audio import Audio
from modules.SysbenchFileIO import SysbenchFileIO
from modules.LogModule import log_warn, log_info, start_time
from time import sleep, time
import subprocess
import socket
import json

MODULE_LAN=True
MODULE_WLAN=True
MODULE_HDMI_VIDEO=True
MODULE_TFT_ANIMATION=True
MODULE_AUDIO=True
MODULE_BLUETOOTH_AUDIO=True
MODULE_SSD_FILEIO=True

LAN_LIMIT_MBPS="1000M"
WLAN_LIMIT_MBPS="1000M"

HEADSET_SINK="alsa_output.platform-bcm2835_audio.analog-stereo"
HEADSET_FREQUENCY="400"
HEADSET_VOLUME="90%"

BLUETOOTH_MAC="20:64:DE:84:11:2C"
BLUETOOTH_SINK="bluez_sink.20_64_DE_84_11_2C.a2dp_sink"
BLUETOOTH_FREQUENCY="400"
BLUETOOTH_VOLUME="90%"

FILEIO_DIRECTORY="/media/pi/TESLADRIVE/sysbench"

I = 0

class Client:
    def __init__(self):
        self.modules = []

        if MODULE_LAN:
            self.iperf_lan = IPerfClient("192.168.1.1", 10024, "logs/iperf_lan.log", "eth0", LAN_LIMIT_MBPS)
            self.iperf_lan.name = "LAN"
            self.modules.append(self.iperf_lan)
        
        if MODULE_WLAN:
            self.iperf_wlan = IPerfClient("192.168.2.1", 10025, "logs/iperf_wlan.log", "wlan0", WLAN_LIMIT_MBPS)
            self.iperf_wlan.name = "WLAN"
            self.modules.append(self.iperf_wlan)

        if MODULE_HDMI_VIDEO:
            self.mplayer = MPlayer("logs/mplayer.log")
            self.modules.append(self.mplayer)
        
        if MODULE_TFT_ANIMATION:
            self.glxgears = GLXGears("logs/glxgears.log")
            self.modules.append(self.glxgears)

        if MODULE_BLUETOOTH_AUDIO:
            run("bluetoothctl power on")
            run("bluetoothctl agent on")
            run("bluetoothctl connect {0}".format(BLUETOOTH_MAC))
            self.bluetooth_audio = Audio(BLUETOOTH_SINK, BLUETOOTH_FREQUENCY, BLUETOOTH_VOLUME)
            self.bluetooth_audio.name = "Bluetooth"
            self.modules.append(self.bluetooth_audio)

        if MODULE_AUDIO:
            self.headset_audio = Audio(HEADSET_SINK, HEADSET_FREQUENCY, HEADSET_VOLUME)
            self.headset_audio.name = "Headset"
            self.modules.append(self.headset_audio)

        if MODULE_SSD_FILEIO:
            self.sysbench_file_io = SysbenchFileIO(FILEIO_DIRECTORY, "/home/pi/emv-client/logs/fileio.log")
            self.modules.append(self.sysbench_file_io)
        
        log_info("Started with the following modules: {0}".format(", ".join(m.name for m in self.modules)))

    def stop(self):
        for module in self.modules:
            log_info("Stopping {0}".format(module.name))
            module.stop()

    def report_status(self):
        global I

        module_statuses = []
        for module in self.modules:
            if module.status():
                module_statuses.append([module.name, "OK"])
            else:
                module_statuses.append([module.name, "ERROR"])
                log_warn("Module {0} is not running".format(module.name))

        # Always restart audio stuff if theres bluetooth to fix potential problems
        if I >= 30:
            I = 0
            if MODULE_BLUETOOTH_AUDIO:
                if not self.bluetooth_audio.status():
                    log_warn("Bluetooth Device is not connected, trying to reconnect")
                    code = run("bluetoothctl connect {0}".format(BLUETOOTH_MAC)).returncode
                    if code == 0: 
                        self.bluetooth_audio.set_volume()
                    else: 
                        return module_statuses
                
                # Stopping one stops all so we only stop once
                self.bluetooth_audio.stop()
                self.bluetooth_audio.start()
                if MODULE_AUDIO:
                    self.headset_audio.start()
        else:
            I = I + 1

        return module_statuses

def run(command):
    return subprocess.run(command, shell=True)

def send_tcp(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
    return response

def loop():
    status = client.report_status()
    status.append(["Time", str(round(time() - start_time()))])
    if MODULE_WLAN:
        status.append(["WIFI Loss", client.iperf_wlan.get_retry_perc()])
    if MODULE_LAN:
        status.append(["LAN Loss", client.iperf_lan.get_retry_perc()])

    try:
        response = send_tcp("192.168.1.1", 10023, json.dumps(status))
        if response == "exit":
            log_info("Exit message received.")
            return -1
    except:
        log_warn("Status Server unreachable")
    
    sleep(0.9)
    return 0
    
if __name__ == "__main__":
    client = Client()
    while True:
        try:
            if loop() == -1:
                break
        except KeyboardInterrupt:
            break
    
    client.stop()
    log_info("Sucessfully exiting.")
    