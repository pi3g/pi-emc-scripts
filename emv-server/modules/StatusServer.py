import threading
import socketserver
import json
import PySimpleGUI as sg
from modules.LogModule import log_info

wants_to_exit = False

colors = {
    "OK": "green",
    "ERROR": "red"
}

layout = [
        [sg.Text("IPerfClient WLAN: ", font=["normal", 24], key="IPerfClient WLAN")],
        [sg.Text("IPerfClient LAN: ", font=["normal", 24], key="IPerfClient LAN")],
        [sg.Text("MPlayer: ", font=["normal", 24], key="MPlayer")],
        [sg.Text("GLXGears: ", font=["normal", 24], key="GLXGears")],
        [sg.Text("Headset Audio: ", font=["normal", 24], key="Headset Audio")],
        [sg.Text("Bluetooth Audio: ", font=["normal", 24], key="Bluetooth Audio")],
        [sg.Text("SysbenchFileIO: ", font=["normal", 24], key="SysbenchFileIO")],
        [sg.Button("Exit", font=["normal", 20]), sg.Text("", font=["normal", 24], key="Time")],
    ]

window = sg.Window(title="Status", layout=layout, 
    finalize=True, auto_size_buttons=True, 
    auto_size_text=True, size=[640, 445], no_titlebar=True,
    location=[0,35]
)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global window
        global wants_to_exit

        data_json = str(self.request.recv(1024), 'ascii')

        if wants_to_exit == True:
            response = bytes("exit", 'ascii')
            self.request.sendall(response)
            window.write_event_value("exit_for_real", "yes")

        data = json.loads(data_json)
        for item in data:
            window.write_event_value(item[0], item[1])
        

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class StatusServer():
    def __init__(self, host, port):
        global window
        window.force_focus()
        self.host = host
        self.port = port
        self.start()

    def start(self):
        self.server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def status(self):
        try:
            running = self.server_thread.is_alive()
        except:
            return False
        if not running:
            self.stop()
            self.start()
        return running
    
    def stop(self):
        self.server.shutdown()
        global window
        window.close()
    
    def loop(self):
        global window
        global wants_to_exit
        global colors
        event, values = window.read(timeout=10)
        if event == sg.WIN_CLOSED or event == 'Exit':
            log_info("Exit Button Pressed")
            wants_to_exit = True
        elif event == "__TIMEOUT__":
            pass
        elif event == "exit_for_real":
            return -1
        elif event == "Time":
            window[event].update("Runtime " + values[event] + "s")
        else:
            window[event].update("{0}: {1}".format(event, values[event]), colors[values[event]])
            
