# --------------------------------File on Robot---------------------------------
# Hosts a TCP connection and interprets the data recieved
import ArmControlLib as ACL
import sys
import os
import sys
import os
import socket
import time
import RoboPiLib_pwm as RPL
RPL.RoboPiInit("/dev/ttyAMA0", 115200)


freq = 3000

## Motor 1 ##
motor1 = ACL.Brushless_Encoded_Motor(0, 1, 26, 20, 1000, 1000, 21848.88, freq)


## Motor2 ##
motor2 = ACL.Brushless_Encoded_Motor(2, 3, 19, 16, 1000, 1000, 11098.56, freq)

motor3 = ACL.Continous_Rotation_Servo(4, 500)
motor4 = ACL.Continous_Rotation_Servo(5, 500)
motor5 = ACL.Continous_Rotation_Servo(6, 500)
motor6 = ACL.Continous_Rotation_Servo(7, 500)

motors = [motor1, motor2, motor3, motor4, motor5, motor6]

IKI = ACL.Inverse_Kinimatics(12.0, 12.0, motor1, motor2, 0, 0)

######################
##    Host Info     ##
######################
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
host = sys.argv[1]
server_address = (host, 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

######################
##      Main        ##
######################

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'client connected:', client_address
        while True:
            data = connection.recv(30)
            data = data.split(' ')
            i = 0
            for motor in motors:
                motor.run(int(data[i]))
                i += 1
                time.sleep(0.01)

    finally:
        connection.close()
