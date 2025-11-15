from .modem_mode import ModemMode
from .udp_mode import UDPMode

def get_mode(mode_name, baud=256, bind_socket=False, ip="localhost", port=5005):
    if mode_name == "modem":
        return ModemMode(baud=baud)
    elif mode_name == "udp":
        return UDPMode(ip=ip, port=port, bind_socket=bind_socket)
    else:
        raise ValueError(f"Unsupported mode: {mode_name}")