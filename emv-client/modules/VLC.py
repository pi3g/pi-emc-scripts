from modules.ModuleBase import ModuleBase

COMMAND="cvlc --loop video.mp4 --no-audio >> {0} 2>&1"

class VLC(ModuleBase):
    def __init__(self, logfile: str):
        ModuleBase.__init__(self, COMMAND.format(logfile), "VLC")
        self.start()