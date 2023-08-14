from modules.ModuleBase import ModuleBase

#COMMAND="DISPLAY=:0 glxgears -fullscreen >> {0} 2>&1"
COMMAND="while true; do cat /dev/urandom > /dev/fb1 2> /dev/null; sleep 0.1; done"

class GLXGears(ModuleBase):
    def __init__(self, logfile: str):
        ModuleBase.__init__(self, COMMAND.format(logfile), "GLXGears")
        self.start()
