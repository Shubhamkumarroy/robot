import cv2
from picamera2 import Picamera2
import numpy as np
import socket
import time

def capture_frame(camera):
	frame = camera.capture_array()
	frame = cv2.flip(frame, 0) # vertical flip
	frame = cv2.flip(frame, 1) # horizontal flip
	return frame
	
def send_frame(client_socket, frame):
	# Encode the frame as JPEG
	_, buffer = cv2.imencode('.jpg', frame)
	data = np.array(buffer).tobytes()
	size = len(data)
	client_socket.sendall(size.to_bytes(4, byteorder='big'))
	client_socket.sendall(data)
	

def serve_frame(host, port):
	while True:
		server_socket.listen(10)
		print("Waiting for a connection...")
		# Accept the client connection
		client_socket, client_address = server_socket.accept()
		print("Connected to:", client_address)
		camera = Picamera2()
		camera.resolution = (640, 480)	
		camera.start()
		# Send the camera resolution
		client_socket.sendall(f"{camera.resolution[0]}, {camera.resolution[1]}".encode())
		#camera.stop()
		try:
			while True:
				request = client_socket.recv(1024)
				if (request == b'next_frame'):
					frame = capture_frame(camera)
					send_frame(client_socket, frame)
				elif (request == b'quit'):
					print('terminating...')
					break
			client_socket.close()
			camera.close()
			time.sleep(1e-3)
		except:
			client_socket.close()
			camera.stop()
			camera.close()

host = '0.0.0.0'
port = 12346

# Create Server Socket Object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific address and port
server_socket.bind((host, port))

try:
	serve_frame(host, port)
except:
	server_socket.close()
