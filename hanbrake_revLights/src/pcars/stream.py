from pcars.packet import Packet
from io import BytesIO
from threading import Thread
import socket
import struct


_MCAST_ANY = "224.0.0.1"


class PCarsStreamReceiver(Thread):

    def __init__(self, port=5606):
        super(PCarsStreamReceiver, self).__init__()
        self.port = port
        self.setDaemon(True)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to the server address
        self.sock.bind(("", self.port))
        group = socket.inet_aton(_MCAST_ANY)
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def getValues(self):
        data = self.sock.recv(1400)
        packet = Packet.readFrom(BytesIO(data))

        return packet._data["rpm"], packet._data["maxRpm"]
            
            
