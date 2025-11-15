import socket
from .interface import ModeInterface

class UDPMode(ModeInterface):
    """
    Mode that uses UDP to send/receive data via Starlink. 
    """

    def __init__(self, ip="0.0.0.0", port=5005):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (ip, port)

    def send(self, data: bytes):
        self.sock.sendto(data, self.addr)

    def receive(self):
        self.sock.bind(self.addr)
        data, _ = self.sock.recvfrom(4096)
        return data

    def close(self): 
        self.sock.close()