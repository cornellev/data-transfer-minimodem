import subprocess, queue, time, threading 
import schema.example_pb2 as example_pb2 

baud = 200
START = b"\x02"   
END   = b"\x03"  

packets = queue.Queue()

def producer():
    """
    Serialize and push (dummy) packets of sensor data to the queue
    """

    # Hardcoded two packets
    for i in range(1, 3):
        msg = example_pb2.Example(
            field1=(i),
            field2=float(i),
            field3=str(i)
        )

        data = msg.SerializeToString()
        packets.put(data)

        time.sleep(1.0)

def consumer():
    """
    Transmit the packets of sensor data to the receiver 
    """

    for _ in range(2):
        cur = packets.get()
        data = START + cur + END 

        subprocess.run(
            ["minimodem", "--tx", str(baud), "-f", "test.wav"], 
            input=data, 
            text=False
        )

def main():
    prod_thread = threading.Thread(target=producer, daemon=True)
    cons_thread = threading.Thread(target=consumer, daemon=True)

    prod_thread.start()
    cons_thread.start()

    prod_thread.join()
    cons_thread.join()

if __name__ == "__main__":
    main()






