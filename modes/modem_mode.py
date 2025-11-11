import subprocess, time
import schema.data_pb2 as data_pb2 
from config import BAUD, START, END, RECEIVER_NUMBER

class ModemMode():
    def __init__(self, baud=256):
        self.baud = baud

    def send(self, data: bytes):
        proc = subprocess.Popen(
            ["minimodem", "--tx", str(self.baud)],
            stdin=subprocess.PIPE,
            text=False
        )
        n = 10
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
                print(str(len(data)))
                seconds_in_message = (len(data) * 8) / self.baud
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


    def receive(self):
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
