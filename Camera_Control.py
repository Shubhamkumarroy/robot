import RPi.GPIO as GPIO
import socket
import pickle
import time

HOST = '0.0.0.0'
PORT = 12347

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
tiltPin = 3
panPin = 4
GPIO.setup(tiltPin, GPIO.OUT)
GPIO.setup(panPin, GPIO.OUT)
tiltPWM = GPIO.PWM(tiltPin, 50)
panPWM = GPIO.PWM(panPin, 50)
tiltPWM.start(0)
panPWM.start(0)

try:
	while True:
		server_socket.listen(10)
		print("server is listening...")
		# Accept a client connection
		client_socket, client_address = server_socket.accept()
		print("Connected to:", client_address)
		try:
			while True:
				received_commands = client_socket.recv(1024)
				servo, angle = pickle.loads(received_commands)
				angle += 90
				dutyCycle = angle/18. + 2.
				if (servo == "panServo"):
					print("Changing panAngle to:", angle)
					panPWM.ChangeDutyCycle(dutyCycle)
					time.sleep(0.02)
					panPWM.ChangeDutyCycle(0)
				if (servo == "tiltServo"):
					print("Changing tiltAngle to:", angle)
					tiltPWM.ChangeDutyCycle(dutyCycle)
					time.sleep(0.01)
					tiltPWM.ChangeDutyCycle(0)
		except:
			panPWM.ChangeDutyCycle(7.)
			time.sleep(0.5)
			panPWM.ChangeDutyCycle(0)
			time.sleep(0.01)
			tiltPWM.ChangeDutyCycle(7.)
			time.sleep(0.5)
			tiltPWM.ChangeDutyCycle(0)
			time.sleep(0.01)
			client_socket.close()
except:
	server_socket.close()
	GPIO.cleanup()
