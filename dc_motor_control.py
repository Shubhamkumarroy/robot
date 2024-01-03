from AMSpi import AMSpi
import socket
import pickle

HOST = '0.0.0.0'
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))
if __name__ == '__main__':
    # Calling AMSpi() we will use default pin numbering: BCM (use GPIO numbers)
    # if you want to use BOARD numbering do this: "with AMSpi(True) as amspi:"
    with AMSpi() as amspi:
        # Set PINs for controlling shift register (GPIO numbering)
        amspi.set_74HC595_pins(21, 20, 16)
        # Set PINs for controlling all 4 motors (GPIO numbering)p
        amspi.set_L293D_pins(5, 6, 13, 19)
        def brake():
            print("Braking.....")
            amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
        try:
            while True:
                # Start listening for incoming connections
                server_socket.listen(10)
                print('server is listening.....')
                # Accept a client connection
                client_socket, client_address = server_socket.accept()
                try:
                    while True:
                        received_commands = client_socket.recv(1024)
                        command, sp = pickle.loads(received_commands)
                        # Process the received command
                        if (command == 'backward'):
                            print("GOING: Backward with speed", sp)
                            amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], speed=sp)
                        elif (command == 'forward'):
                            print("GOING: Forward with speed", sp)
                            amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], clockwise=False, speed=sp)
                        elif (command == 'right'):
                            print('TURNING: Right with speed', sp)
                            amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3], speed=sp)
                            amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4], clockwise=False, speed=sp)
                        elif (command == 'left'):
                            print('TURNING: Left with speed', sp)
                            amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3], clockwise=False, speed=sp)
                            amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4], speed=sp)
                        elif (command == 'brake'):
                            brake()
                        else:
                            brake()
                except:
                    brake()
                    client_socket.close()
        except:
            server_socket.close()
