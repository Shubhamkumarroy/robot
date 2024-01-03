import cv2
import socket
import numpy as np

def capture_frame():
	frame_cap = cv2.VideoCapture(0)
	ret, frame = frame_cap.read()
	frame_cap.release()
	return ret, frame

def send_frame(client_socket, frame):
	# Encode the frame as JPEG
	_, buffer = cv2.imencode('.jpg', frame)
	data = np.array(buffer).tobytes()
	size = len(data)
	client_socket.sendall(size.to_bytes(4, byteorder='big'))
	client_socket.sendall(data)
	
def serve_frame(host, port):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((host, port))
	# Open the camera to capture frame
	frame_cap = cv2.VideoCapture(0)
	# Set the video width and height
	frame_width = int(frame_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(frame_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	frame_cap.release()
	while True:
		server_socket.listen(10)
		print("Waiting for a connection...")
		# Accept the client connection
		client_socket, client_address = server_socket.accept()
		print("Connected to:", client_address)
		# Send the video width and height to the client
		client_socket.sendall(f"{frame_width}, {frame_height}".encode())
		while True:
			# Receive request from the client
			try:
				request = client_socket.recv(1024)
			except:
				break
			if (request == b'next_frame'):
				# Read the next frame from the camera
				ret, frame = capture_frame()
				if (not ret):
					print("Error in capturing frame...")
					break
				# Send the frame to the client
				try:
					send_frame(client_socket, frame)
				except:
					break
			elif (request == b'quit'):
				print("Terminating...")
				break
		client_socket.close()
	# Release the frame capture and close the connection and socket
	frame_cap.release()
	server_socket.close()
	
host = '0.0.0.0'
port = 12346
serve_frame(host, port)
