import subprocess, time
import schema.data_pb2 as data_pb2 

baud = 300
START = b"\x02"   
END   = b"\x03"  

def main():
    proc = subprocess.Popen(
        ["minimodem", "--tx", str(baud)],
        stdin=subprocess.PIPE,
        text=False
    )
    count = 0

    try:
        while count < 10:

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
            seconds_in_message = (len(data) * 8) / baud
            t_time = 1 - seconds_in_message
            print(str(seconds_in_message))

            if t_time < 0:
                raise ValueError("Message is too long for the given baud rate")

            proc.stdin.write(data)
            proc.stdin.flush()

            print(f"Sent packet #{count + 1}")
            count += 1
            time.sleep(t_time)
    finally:
        if proc.stdin:
            proc.stdin.close()
        proc.wait()

if __name__ == "__main__":
    main()






