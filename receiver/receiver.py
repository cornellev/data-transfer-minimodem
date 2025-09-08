import subprocess
import schema.data_pb2 as data_pb2

baud = 200
START = b"\x02"   
END   = b"\x03"  

def main():
    proc = subprocess.Popen(
        ["minimodem", "--rx", "-8", str(baud)],
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
                    msg = data_pb2.Example()
                    msg.ParseFromString(packet)
                    print(msg)
                except Exception as e:
                    print("Failed to parse packet:", e)
                
                raw = raw[end+1:]

    finally:
        proc.terminate()


if __name__ == "__main__":
    main()