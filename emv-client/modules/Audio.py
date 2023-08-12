from modules.ModuleBase import ModuleBase
import subprocess

START="XDG_RUNTIME_DIR=/run/user/1000 /usr/bin/pactl load-module module-sine sink={0} frequency={1} >> logs/audio.log 2>&1"
STOP="XDG_RUNTIME_DIR=/run/user/1000 /usr/bin/pactl unload-module module-sine >> logs/audio.log 2>&1"
SET_VOLUME="XDG_RUNTIME_DIR=/run/user/1000 /usr/bin/pactl set-sink-volume {0} {1} >> logs/audio.log 2>&1"

class Audio(ModuleBase):
    def __init__(self, sink: str, frequency: str, volume: str):
        ModuleBase.__init__(self, START.format(sink, frequency), "Audio")
        self.sink = sink
        self.frequency = frequency
        self.volume = volume
        self.set_volume()
        self.start()

    def stop(self):
        return subprocess.run(STOP.format(), shell=True).returncode

    def set_volume(self):
        return subprocess.run(SET_VOLUME.format(self.sink, self.volume), shell=True).returncode
    
    def status(self):
        return self.set_volume() == 0
