# --------------------------------File on client--------------------------------
# Reads

import ArmControlLib as ACL
import ftplib
import RoboPiLib_pwm as RPL
import time
RPL.RoboPiInit("/dev/ttyAMA0", 115200)
ftp = ftplib.FTP('192.168.21.225', 'jwrickman18',
                 'Heap!860')  # host computer info
# directory of repo on host
ftp.cwd('/Users/jwrickman18/Desktop/code/robo-control')
freq = 3000
## Motor 1 ##
motor1 = ACL.Motor(0, 1, 26, 20, 1000, 1000, 21848.88, freq)


## Motor2 ##
motor2 = ACL.Motor(2, 3, 19, 16, 1000, 1000, 11098.56, freq)

a = True
while a:
    gFile = open("ftpTemp.txt", "wb")
    try:
        ftp.retrbinary('RETR ftpTemp.txt', gFile.write)
    except:
        print "issue with ftp.retrbinary line 25"
    gFile.close()
    ftp.quit()
    gFile = open("ftpTemp.txt", "r")
    buff = gFile.read()
    gFile.close()
    convertTxtArray = buff.split()
    motor1_count_request = convertTxtArray[0]
    print motor1_count_request
    motor2_count_request = convertTxtArray[1]
    print motor2_count_request
    latency = time.time() - float(convertTxtArray[2])
    motor1.move_to_position(motor1_count_request)
    motor2.move_to_position(motor2_count_request)
    print latency
    print "Worked one time"
    timeStart = time.time()
    time.sleep(0.01)
    if time.time() - timeStart > 1:
        print "Motor1 rot count: %d Motor2 rot count: %d" % (
            motor1.encoder.Rotary_counter, motor2.encoder.Rotary_counter)
        timeStart = time.time()
