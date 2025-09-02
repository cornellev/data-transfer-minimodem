import subprocess
import schema.example_pb2 as example_pb2

def main():

    baud = 200
    proc = subprocess.Popen(
        ["minimodem", "--rx", "-8", str(baud)],
        stdout=subprocess.PIPE
    )

    START = b"\x02"   
    END   = b"\x03"   
    raw= b""

    while True:
        byte = proc.stdout.read(1)
        if not byte:
            break
            
        raw += byte 

        if START in raw and END in raw:
            start = raw.find(START) + 1
            end = raw.find(END, start)
            raw_bytes = raw[start:end]

            msg = example_pb2.Example()
            msg.ParseFromString(raw_bytes)

            print(msg)
            break
    
    proc.terminate()


if __name__ == "__main__":
    main()