import signal
import sys
from time import sleep

from AbstractVirtualCapability import AbstractVirtualCapability, VirtualCapabilityServer, formatPrint

class ChargeStation(AbstractVirtualCapability):
    def __init__(self, server: VirtualCapabilityServer):
        super().__init__(server)
        self.uri = "ChargeStation"
        self.functionality = {"get_pos": None}

    def GetPosition(self, params: dict):
        return {"Position3D": self.functionality["get_pos"]()}

    def loop(self):
        sleep(.0001)

if __name__ == '__main__':
    # Needed for properly closing when process is being stopped with SIGTERM signal
    def handler(signum, frame):
        print("[Main] Received SIGTERM signal")
        listener.kill()
        quit(1)
    try:
        port = None
        if len(sys.argv[1:]) > 0:
            port = int(sys.argv[1])
        server = VirtualCapabilityServer(port)
        listener = ChargeStation(server)
        listener.start()
        signal.signal(signal.SIGTERM, handler)
        listener.join()
    # Needed for properly closing, when program is being stopped wit a Keyboard Interrupt
    except KeyboardInterrupt:
        print("[Main] Received KeyboardInterrupt")
        server.kill()
        listener.kill()