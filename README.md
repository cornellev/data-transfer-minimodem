# Data Transfer - Modem | FA25

Audio-based data transfer system using [minimodem](https://www.whence.com/minimodem/).  
This system serializes structured vehicle sensor data using Protocol Buffers, encodes it into audio tones via minimodem using Frequency-Key Shifting (FSK) modulation, and then receives/decodes it back into readable data to be visualized on the Race Engineer Dashboard.
This is meant to be a backup to the primary data stream (Starlink) viewed by the race engineer during competition.

---

## Installation

Windows users: minimodem does not run natively on Windows. Please install WSL2 with Ubuntu and run this project inside the WSL terminal.

```bash
git clone https://github.com/cornellev/data-transfer-minimodem.git
cd data-transfer-minimodem
```

Install dependencies:
```bash
# macOS
brew install minimodem

# Windows/Linux (Ubuntu)
sudo apt-get install minimodem

pip install -r requirements.txt
```

---

## How to Run

#### Sending Data 
Run the sender module to serialize a message and transmit it with minimodem:
```bash
python3 -m sender.sender
```

#### Receiving Data 
Run the receiver module to listen for incoming data, decode it, and deserialize it:
```bash
python3 -m receiver.receiver
```

---

## Project Structure
```
DATA-TRANSFER-MINIMODEM/
│
├── receiver/              # Receiver code 
│   └── receiver.py
│
├── schema/                # Protobuf schema definitions
│   ├── data.proto
│   ├── data_pb2.py
│   └── __init__.py
│
├── sender/                # Sender code 
│   └── sender.py
│
├── cellular_modem.py      # CellularModem class 
├── config.py              # Data/voice call configurations
├── README.md              
├── requirements.txt       
└── .gitignore             
```
---

## Adding/Editing Protobuf Schemas
This system uses [Protocol Buffers](https://protobuf.dev/getting-started/pythontutorial/) to define structured messages.
To add or edit a schema, modify the `.proto` file in `/schema`, then regenerate the Python bindings:
```bash
protoc --python_out=schema schema/data.proto
```



