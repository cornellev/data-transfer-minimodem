import subprocess
import schema.data_pb2 as data_pb2 
from config import BAUD, START, END
from cellular_modem import CellularModem

def receive_packets():
    """Receive and print packets of data via minimodem."""
    proc = subprocess.Popen(
        ["minimodem", "--rx", "-8", str(BAUD)],
        stdout=subprocess.PIPE
    )

    raw= b""

    try: 
        while True:
            byte = proc.stdout.read(1)
            if not byte:
                break
                
            raw += byte 

            while START in raw and END in raw:
                start = raw.find(START) + 1
                end = raw.find(END, start)
                packet = raw[start:end]

                try: 
                    msg = data_pb2.Sensors()
                    msg.ParseFromString(packet)
                    print(str(len(msg)))
                except Exception as e:
                    print("Failed to parse packet:", e)
                
                raw = raw[end+1:]

    finally:
        proc.terminate()

def main():
    modem = CellularModem(power_key=6, port="/dev/ttyS0", baud=115200)

    try:
        modem.power_on()

        if modem.answer_call():
            print("Call answered. Packets received:")
            receive_packets()
            modem.hangup()
    finally:
        modem.power_down()
        modem.close()


if __name__ == "__main__":
    main()