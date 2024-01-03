import cv2
import numpy as np
import socket

def send_video(host, port):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to a specific address and port
	server_socket.bind((host, port))
	# Open the video capture
	video_capture = cv2.VideoCapture(0)
	# Set the video width and height
	video_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
	video_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
	while True:
		server_socket.listen(10)
		print("Waiting for a connection...")
		# Accept the client connection
		client_socket, client_address = server_socket.accept()
		print("Connected to:", client_address)
		# Send the video width and height to the client
		client_socket.sendall(f"{video_width}, {video_height}".encode())
		while True:
			# Read a frame from the video capture
			ret, frame = video_capture.read()
			if (not ret):
				print("Error in reading frame...")
				break
			# Convert the frame into JPEG format
			_, buffer = cv2.imencode('.jpg', frame)
			# Convert the buffer to bytes and get the size
			data = np.array(buffer).tobytes()
			size = len(data)
			# Send the size of the frame to the client
			try:
				client_socket.sendall(size.to_bytes(4, byteorder='big'))
				# Send the frame data to the client
				client_socket.sendall(data)
			except:
				break
			if (cv2.waitKey(1) & 0xFF == ord('q')):
				break
		client_socket.close()
	# Release the video capture and close the connection and socket
	video_capture.release()
	server_socket.close()

host = '0.0.0.0'
port = 12346
send_video(host, port)
