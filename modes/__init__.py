from .modem_mode import ModemMode
from .udp_mode import UDPMode

def get_mode(mode_name, baud=None, ip="127.0.0.1", port=5005):
    if mode_name == "modem":
        return ModemMode(baud=baud)
    elif mode_name == "udp":
        return UDPMode(ip=ip, port=port)
    else:
        raise ValueError(f"Unsupported mode: {mode_name}")
