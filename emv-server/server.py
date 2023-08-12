from modules.IPerfServer import IPerfServer
from modules.StatusServer import StatusServer
from modules.LogModule import log_warn, log_info
from time import sleep
import os

wlan_problem = False

class Server:
    def __init__(self):
        self.status_server = StatusServer("192.168.1.1", 10023)
        self.iperf_lan = IPerfServer(10024, "logs/iperf_lan.log")
        self.iperf_wlan = IPerfServer(10025, "logs/iperf_wlan.log")
    
    def stop(self):
        self.status_server.stop()
        self.iperf_lan.stop()
        self.iperf_wlan.stop()

    def status_check(self):
        global wlan_problem

        if not server.iperf_lan.status():
            log_warn("LAN Iperf not running")

        if not server.iperf_wlan.status():
            log_warn("WLAN Iperf not running")

        if not server.status_server.status():
            log_warn("Status Server is not running")

        try:
            os.popen("ip addr show wlan0").read().split("inet ")[1].split("/")[0]
            if wlan_problem: # If we had a wlan problem restart iperf
                server.iperf_wlan.stop()
                sleep(1)
                server.iperf_wlan.start()
                wlan_problem = False
        except:
            wlan_problem = True
            log_warn("Interface wlan0 has no valid ip")

if __name__ == "__main__":
    server = Server()

    i = 0
    while True:
        try:
            sleep(0.1)
            
            if server.status_server.loop() == -1:
                break

            i = i + 1
            if i > 100:
                i = 0
                server.status_check()
        except KeyboardInterrupt:
            break

    server.stop()
