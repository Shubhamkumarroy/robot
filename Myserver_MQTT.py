import cv2
from picamera2 import Picamera2
import numpy as np
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("camera/control")
    else:
        print("Failed to connect, return code: ", rc)
        
def on_message(client, userdata, msg):
    if msg.topic == "camera/control":
        command = msg.payload.decode("utf-8")
        if command == "next_frame":
            frame = capture_frame(camera)
            send_frame(frame)
            
def capture_frame(camera):
	camera.start()
	frame = camera.capture_array()
	frame = cv2.flip(frame, 0)
	camera.stop()
	return frame
	
def send_frame(frame):
    # Encode the frame as JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    data = np.array(buffer).tobytes()
    client.publish("camera/frame", data, qos=1)
    
def serve_frame():
    client.loop_start()
    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Server stopped by the user")
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        client.loop_stop()
        client.disconnect()
        
# Create MQTT client
client = mqtt.Client()

# Set MQTT broker address
broker_address = "localhost"
broker_port = 1883

# Set MQTT client callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker_address, broker_port, 60)

camera = Picamera2()
camera.resolution = (640, 480)

try:
	serve_frame()
finally:
	camera.stop()
