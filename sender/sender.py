import argparse, time
from config import BAUD, START, END, RECEIVER_NUMBER
from cellular_modem import CellularModem
from schema import data_pb2
from modes import get_mode

def dummy_packet(count: int):
    """
    Return one dummy protobuf packet as bytes with START/END markers. 
    """
    msg = data_pb2.Sensors(
                voltage=1.0 + count,
                draw=2.0 + count,
                gps_lat=3.0 + count,
                gps_long=4.0 + count,
                velocity=5.0 + count,
                throttle=6.0 + count,
            )
    return START + msg.SerializeToString() + END

def main():
    parser = argparse.ArgumentParser(description="Send data via UDP or Modem")
    parser.add_argument(
        '--mode', 
        choices=['udp', 'modem'], 
        required=True, 
        help="Transmission mode: 'udp' or 'modem'"
    )
    args = parser.parse_args()

    mode = get_mode(args.mode, baud=BAUD)
    n = 10 # number of dummy protobuf packets to send 

    def send_loop():
        """
        Send each packet as they are being generated.
        """
        for count in range(n):
            packet = dummy_packet(count)
            mode.send(packet)
            time.sleep(1)
    
    if mode == 'modem':
        modem = CellularModem(power_key=6, port="/dev/ttyS0", baud=115200)
        try:
            modem.power_on()
            if modem.dial(RECEIVER_NUMBER):
                print("Call connected. Sending packets:")
                send_loop()
                modem.hangup()
        finally:
            modem.power_down()
            modem.close()
            mode.close()
    elif mode == 'udp':
        send_loop()
        mode.close()   

if __name__ == "__main__":
    main()






