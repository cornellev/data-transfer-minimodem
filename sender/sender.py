import subprocess 
import schema.example_pb2 as example_pb2

def main():

    msg = example_pb2.Example(field1=1, field2=1.0, field3="Test")
    data = msg.SerializeToString()
    baud = 300

    subprocess.run(["minimodem", "--tx", str(baud)], input=data)

if __name__ == "__main__":
    main()






