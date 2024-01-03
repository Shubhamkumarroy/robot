import socket
import time
import RPi.GPIO as GPIO  # Import the GPIO library

# Initialize GPIO for the ultrasonic sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
TRIG=18
ECHO=16
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def measure_distance():
    # Trigger the ultrasonic sensor to measure distance
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    distance=int(distance)
    return distance

def serve_distance(host, port):
    while True:
        serve_socket.listen(10)
        print("Waiting for a connection...")
        # Accept the client connection
        client_socket, client_address = serve_socket.accept()
        print("Connected to:", client_address)
        
        try:
            while True:
                request = client_socket.recv(1024)
                if request == b'get_distance':
                    distance = measure_distance()
                    client_socket.sendall(str(distance).encode())
                elif request == b'quit':
                    print('Terminating...')
                    break
            client_socket.close()
            time.sleep(0.01)
        except:
            client_socket.close()

host = '0.0.0.0'
port = 12347

# Create serve Socket Object
serve_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific address and port
serve_socket.bind((host, port))

try :
    serve_distance(host, port)
except KeyboardInterrupt :
    pass
finally:
    serve_socket.close()
    GPIO.cleanup()  # Cleanup GPIO on program exit

