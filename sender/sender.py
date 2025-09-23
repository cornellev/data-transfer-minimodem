import subprocess, time
import schema.data_pb2 as data_pb2 
from config import BAUD, START, END, RECEIVER_NUMBER
from cellular_modem import CellularModem

def send_packets(n):
    """Send n packets of protobuf data via minimodem."""
    proc = subprocess.Popen(
        ["minimodem", "--tx", str(BAUD)],
        stdin=subprocess.PIPE,
        text=False
    )
    count = 0

    try:
        while count < n:

            # Dummy data 
            msg = data_pb2.Sensors(
                voltage=1.0 + count,
                draw=2.0 + count, 
                gps_lat=3.0 + count,
                gps_long=4.0 + count,
                velocity=5.0+count,
                throttle=6.0+count
            )

            data = START + msg.SerializeToString() + END 
            seconds_in_message = (len(data) * 8) / BAUD
            t_time = 1 - seconds_in_message

            if t_time < 0:
                raise ValueError("Message is too long for the given baud rate")

            proc.stdin.write(data)
            proc.stdin.flush()

            count += 1
            time.sleep(t_time)
    finally:
        if proc.stdin:
            proc.stdin.close()
        proc.wait()

def main():
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

if __name__ == "__main__":
    main()






