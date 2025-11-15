import argparse, time
import schema.data_pb2 as data_pb2 
from config import START, END, BAUD
from modes import get_mode 

def process_packet(raw: bytes):
    """
    Decode and print a protobuf packet. 
    """
    if not raw:
        return
    start = raw.find(START) + 1
    end = raw.find(END, start)
    packet = raw[start:end]
    try: 
        msg = data_pb2.Sensors()
        msg.ParseFromString(packet)
        print(msg)
    except Exception as e:
        print("Failed to parse packet:", e)

def main():
    parser = argparse.ArgumentParser(description="Receive data via UDP or Modem")
    parser.add_argument(
        '--mode', 
        choices=['udp', 'modem'], 
        required=True, 
        help="Transmission mode: 'udp' or 'modem'"
    )
    args = parser.parse_args()

    mode = get_mode(args.mode, baud=BAUD, bind_socket=True)

    if args.mode == 'modem':
        from cellular_modem import CellularModem
        modem = CellularModem(power_key=6, port="/dev/ttyS0", baud=115200)
        try:
            modem.power_on()
            if modem.answer_call():
                print("Call answered. Packets received:")
                while True:
                    packet = mode.receive()
                    if not packet:
                        break
                    process_packet(packet)
                    time.sleep(0.05)
                modem.hangup()
        finally:
            modem.power_down()
            modem.close()
            mode.close()
    elif args.mode == 'udp':
        try: 
            while True:
                packet = mode.receive()
                if not packet:
                    break
                process_packet(packet)
                time.sleep(0.001)
        finally:
            mode.close()

if __name__ == "__main__":
    main()