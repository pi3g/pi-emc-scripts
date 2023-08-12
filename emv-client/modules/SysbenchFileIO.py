from modules.ModuleBase import ModuleBase
from time import sleep
import subprocess
import os

RATE=300
PREP="cd {0} && sysbench fileio --file-total-size=15G --file-test-mode=rndrw --time=0 --max-requests=0 prepare >> {1} 2>&1"
RUN="cd {0} && sysbench fileio --file-total-size=15G --file-test-mode=rndrw --time=0 --max-requests=0 --rate={1} --report-interval=30 run >> {2} 2>&1"
CLEANUP="cd {0} && sysbench fileio --file-total-size=15G --file-test-mode=rndrw --time=0 --max-requests=0 cleanup >> {1} 2>&1"

class SysbenchFileIO(ModuleBase):
    def __init__(self, directory: str, logfile: str):
        ModuleBase.__init__(self, RUN.format(directory, RATE, logfile), "SysbenchFileIO")
        
        if len(os.listdir(directory)) == 0:
            prep = subprocess.Popen(PREP.format(directory, logfile), preexec_fn=os.setsid, shell=True)
            while prep.poll() is None:
                sleep(1)
        
        self.start()
    
    def cleanup(self):
        self.cleanup = subprocess.Popen(CLEANUP.format(self.directory, self.logfile), preexec_fn=os.setsid, shell=True)
        while self.cleanup.poll() is None:
            sleep(1)
