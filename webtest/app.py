from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
import serial
ser = serial.Serial('COM4', 9600)

"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

if ser.is_open:
    print("Serial port is open.")

distance = 0
"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():
    global distance,ser
    print("Generating random sensor values")
    while True:
        if ser.is_open:
            try:
                arduino = ser.readline().decode().strip()  # Read the data from Arduino
                data = arduino.split('|')  # Split the data into individual values
                if len(data) == 4:
                    distance = data[0]
                    hujan = data[1]
                    flow = data[2]
                    socketio.emit('updateSensorData', {'distance': distance, 'hujan': hujan, 'flow': flow, "date": get_current_datetime()})
                    socketio.sleep(1)
            except :
                print("data not updated")
        else:
            print("data cancceled")

"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)