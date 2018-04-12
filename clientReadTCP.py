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
            data = connection.recv(9)
            data = data.split(' ')
            print data[0]
            if data[0] == 0:
                motor1.stop()
            elif data[0] == 1:
                motor1.clockwise()
            elif data[0] == 2:
                motor1.counterClockwise()
            time.sleep(0.1)

    finally:
        connection.close()
