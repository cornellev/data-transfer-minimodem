import subprocess, time
import schema.data_pb2 as data_pb2 

baud = 200
START = b"\x02"   
END   = b"\x03"  

def main():
    count = 0
    while True:

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

        subprocess.run(
            ["minimodem", "--tx", str(baud)], 
            input=data, 
            text=False
        )

        print(f"Sent packet #{count}")
        count += 1
        time.sleep(1.0)

if __name__ == "__main__":
    main()






