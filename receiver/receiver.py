import subprocess
import schema.example_pb2 as example_pb2

def main():

    baud = 300
    proc = subprocess.run(
        ["minimodem", "--rx", str(baud)],
        capture_output=True
    )

    raw = proc.stdout

    msg = example_pb2.Example()
    msg.ParseFromString(raw)

    print(msg)

if __name__ == "__main__":
    main()