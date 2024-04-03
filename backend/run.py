from flask import Flask, jsonify, request
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import json
import threading
from datetime import datetime
from bson.json_util import dumps

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

        # Check if data is a dictionary
        if not isinstance(data, dict):
            print(f"Unexpected JSON format: {msg.payload}")
            return

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

client.connect("broker.emqx.io", 1883, 60)  # Connect to the MQTT broker

# Subscribe to the topic where the Arduino is publishing the data
client.subscribe("demo")

# Start a loop to process MQTT network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
client.loop_start()

@app.route('/api/data/<start>/<end>', methods=['GET'])
def get_data(start,end):
    startt = float(start)
    endt = float(end)
    if start is None or end is None:
        return jsonify({'status': 'error', 'message': 'Missing start or end parameter'}), 400

    # print(collection.find({'timestamp': {'$gte': startt, '$lte': endt}}))
    data = (collection.find({'timestamp': {'$gte': startt , '$lte': endt}}))
    ret = []
    print(startt, endt)
    for  x in data:
        ret.append({key: value for key, value in x.items() if key != '_id'})

    return jsonify({'status': 'success', 'data': ret}), 200

@app.route('/api/test')
def test():
    return jsonify({'status': 'success', 'data': 'test'}), 200


# @app.route('/api/data', methods=['GET'])
# def get_all_data():
#     data = list(collection.find())
#     return jsonify({'status': 'success', 'data': json.loads(dumps(data))}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0")

# create a new route that will return all the data from the MongoDB database.