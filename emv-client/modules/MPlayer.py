from modules.ModuleBase import ModuleBase

COMMAND="cvlc --loop video.mp4 --no-audio >> {0} 2>&1"

class MPlayer(ModuleBase):
    def __init__(self, logfile: str):
        ModuleBase.__init__(self, COMMAND.format(logfile), "MPlayer")
        self.start()