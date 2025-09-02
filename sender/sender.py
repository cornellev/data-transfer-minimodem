import subprocess 
import schema.example_pb2 as example_pb2

def main():

    msg = example_pb2.Example(field1=1, field2=1.0, field3="Test")
    data = msg.SerializeToString()

    baud = 200

    START = b"\x02"   
    END   = b"\x03"   

    new_data = START + data + END 

    subprocess.run(["minimodem", "--tx", str(baud)], input=new_data, text=False)

if __name__ == "__main__":
    main()






