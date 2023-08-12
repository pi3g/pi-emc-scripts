import subprocess
from signal import SIGTERM
from modules.LogModule import log_warn
import os

class ModuleBase:
    def __init__(self, command, name):
        self.command = command
        self.name = name
    
    def start(self):
        self.process = subprocess.Popen(self.command, preexec_fn=os.setsid, shell=True)

    def stop(self):
        try:
            os.killpg(os.getpgid(self.process.pid), SIGTERM)
        except:
            log_warn("Error stopping {0}".format(self.name))
    
    def status(self):
        running = self.process.poll() == None
        if not running:
            # try restarting but still output the false state
            self.restart()
        return running
    
    def restart(self):
        if self.process.poll() == None:
            self.stop()
        self.start()
