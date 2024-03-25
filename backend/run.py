from flask import Flask
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import json
import threading
from datetime import datetime

app = Flask(__name__)

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017')
db = client['ELET2415']  # Use the 'data' database
collection = db['data']  # Use the 'sensor_data' collection

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        # Parse the JSON data
        data = json.loads(msg.payload)

        # Add a timestamp to the data
        data['timestamp'] = int(datetime.now().timestamp())

        # Insert the data into the MongoDB database
        collection.insert_one(data)

        # Print the received data
        print(data)
        print("\n")
    except json.JSONDecodeError:
        print(f"Could not parse JSON: {msg.payload}")

# Create an MQTT client and attach our routines to it.
client = mqtt.Client(client_id="620151149")
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)  # Connect to the MQTT broker

# Subscribe to the topic where the Arduino is publishing the data
client.subscribe("demo")

# Start a loop to process MQTT network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
client.loop_start()

if __name__ == "__main__":
    app.run()