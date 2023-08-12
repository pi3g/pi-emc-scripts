from modules.ModuleBase import ModuleBase

COMMAND="DISPLAY=:0 glxgears -fullscreen >> {0} 2>&1"

class GLXGears(ModuleBase):
    def __init__(self, logfile: str):
        ModuleBase.__init__(self, COMMAND.format(logfile), "GLXGears")
        self.start()
