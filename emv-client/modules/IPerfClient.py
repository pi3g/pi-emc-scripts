from modules.ModuleBase import ModuleBase
from modules.LogModule import log_warn
import subprocess
import os

COMMAND="/usr/local/bin/iperf3 -c {0} -p {1} --timestamps -i 30 -t 0 --logfile {2} --bind {3} -b {4}"

class IPerfClient(ModuleBase):
    def __init__(self, ip: str, port: str, logfile: str, interface: str, bps: str):
        ModuleBase.__init__(self, COMMAND.format(ip, port, logfile, "", bps), "IPerfClient")
        self.ip = ip
        self.port = port
        self.logfile = logfile
        self.interface = interface
        self.bps = bps
        self.start()

    def start(self):
        try:
            ifip = os.popen("ip addr show {0}".format(self.interface)).read().split("inet ")[1].split("/")[0]
        except:
            ifip = "a"
        self.process = subprocess.Popen(COMMAND.format(self.ip, self.port, self.logfile, ifip, self.bps), preexec_fn=os.setsid, shell=True)

    def status(self):
        try:
            os.popen("ip addr show {0}".format(self.interface)).read().split("inet ")[1].split("/")[0]
        except:
            self.stop()
            log_warn("Interface {0} has no valid ip".format(self.interface))
            return False

        running = self.process.poll() == None
        if not running:
            # try restarting but still output the false state
            self.restart()
        return running