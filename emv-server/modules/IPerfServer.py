import subprocess
from signal import SIGTERM
import os

COMMAND="/usr/local/bin/iperf3 -s -p {0} --rcv-timeout 5000 --timestamps -i 1 --logfile {1}"

class IPerfServer:
    def __init__(self, port: int, logfile: str):
        self.port = port
        self.logfile = logfile
        self.start()
    
    def start(self):
        self.iperf = subprocess.Popen(COMMAND.format(self.port, self.logfile), preexec_fn=os.setsid, shell=True)

    def stop(self):
        os.killpg(os.getpgid(self.iperf.pid), SIGTERM)

    def status(self):
        running = self.iperf.poll() == None
        if not running:
            # try restarting but still output the false state
            self.start()
        return running
