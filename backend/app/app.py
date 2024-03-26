# backend/app/app.py

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/your-endpoint')
def get_data():
    # Replace this with code to get the actual data
    data = {
        'temperature': 20,
        'humidity': 50,
        'altitude': 1000,
        'heat_index': 25,
        'soil_moisture': 30,
    }
    return jsonify(data)