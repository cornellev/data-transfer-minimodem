import subprocess, time
import argparse
import schema.data_pb2 as data_pb2 
from config import BAUD, START, END, RECEIVER_NUMBER
from cellular_modem import CellularModem

from modes.udp_mode import UDPMode
from modes.modem_mode import ModemMode

def get_mode(args):
    if args.mode == 'udp':
        return UDPMode(ip="0.0.0.0", port=5005)
    elif args.mode == 'modem':
        return ModemMode(baud=BAUD)


def main():
    parser = argparse.ArgumentParser(description="Choose UDP or Modem")
    parser.add_argument('--mode', choices=['udp', 'modem'], required=True, help="Transmission mode: 'udp' or 'modem'")

    args = parser.parse_args()
    mode = get_mode(args)
    if args.mode == 'modem':
        modem = CellularModem(power_key=6, port="/dev/ttyS0", baud=115200)

        try:
            modem.power_on()

            if modem.dial(RECEIVER_NUMBER):
                print("Call connected. Sending packets:")
                send_packets(10)
                modem.hangup()
        finally:
            modem.power_down()
            modem.close()

    #if args.mode == 'udp':
    

if __name__ == "__main__":
    main()






