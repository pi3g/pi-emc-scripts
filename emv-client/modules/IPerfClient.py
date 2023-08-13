from modules.ModuleBase import ModuleBase
from modules.LogModule import log_warn
import subprocess
import os
import re

COMMAND="/usr/local/bin/iperf3 -c {0} -p {1} --timestamps -i 1 -t 0 --logfile {2} --bind {3} -b {4}"

PATTERN = r".*sec\s+(\d+ (MBytes|KBytes|GBytes|Bytes)).*\/sec\s+(\d+)\s+.*"
UNITS = {
    "Bytes": 1,
    "KBytes": 1000,
    "MBytes": 1000000,
    "GBytes": 1000000000
}
MTU = 1500  # Based on default MTU

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

    def get_retry_perc(self):
        with open(self.logfile, "rb") as f:
            try:  # catch OSError in case of a one line file 
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()
            
        if match := re.search(PATTERN, last_line):
            transfer = match.group(1).split()
            bytes_transferred = int(float(transfer[0]) * UNITS[transfer[1]])
            retries = int(match.group(3))
            packets_transferred = bytes_transferred // MTU
            loss_percent = retries / packets_transferred

            if loss_percent > 0.10:
                log_warn("Packet Loss over 10%% on " + self.name)
            
            return "{0}%".format(int(loss_percent * 100))
        return ""

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