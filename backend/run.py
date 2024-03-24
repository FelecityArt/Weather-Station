from flask import Flask
from pymongo import MongoClient
import serial
import json
import threading

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017')
db = client['ELET2415']  # Use the 'data' database
collection = db['data']  # Use the 'sensor_data' collection

# Connect to the serial port
ser = serial.Serial('/dev/ttyUSB0', 115200)

def read_from_serial():
    while True:
        # Read a line from the serial port
        line = ser.readline()

        # Decode the line to a string and strip newline characters
        line = line.decode('utf-8').strip()

        if line:  # Check if line is not empty
            try:
                # Parse the JSON data
                data = json.loads(line)

                # Insert the data into the MongoDB database
                collection.insert_one(data)
            except json.JSONDecodeError:
                print(f"Could not parse JSON: {line}")

if __name__ == "__main__":
    app.run()