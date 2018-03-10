# --------------------------------File on client--------------------------------
# Reads

import ArmControlLib as ACL
import ftplib
import RoboPiLib_pwm as RPL
import time
RPL.RoboPiInit("/dev/ttyAMA0", 115200)


def ftpSetup():
    gFile = open("IPinfo.txt", "r")
    buff = gFile.read()
    gFile.close()
    ip_info_array = buff.split()
    ipNum = ip_info_array[0]
    userName = ip_info_array[1]
    passWord = ip_info_array[2]
    return ftplib.FTP(ipNum, userName,
                      passWord)  # host computer info


def ftpInfoUpdate():
    print "Update FTP Info"
    gFile = open("IPinfo.txt", "r+")
    gFile.write(raw_input("IPAddress:"))
    gFile.write(" ")
    gFile.write(raw_input("UserName:"))
    gFile.write(" ")
    gFile.write(raw_input("PassWord"))
    gFile.close()


try:
    ftp = ftpSetup()
except:
    ftpInfoUpdate()
    ftp = ftpSetup()

ftp.cwd('/Users/jwrickman18/Desktop/code/robo-control')
freq = 3000
## Motor 1 ##
motor1 = ACL.Motor(0, 1, 26, 20, 1000, 1000, 21848.88, freq)


## Motor2 ##
motor2 = ACL.Motor(2, 3, 19, 16, 1000, 1000, 11098.56, freq)

IKI = ACL.Inverse_Kinimatics(12.0, 12.0, motor1, motor2)

motor1_count_request_old = 0
motor2_count_request_old = 0


def updateFTPfile():
    gFile = open("ftpTemp.txt", "wb")
    ftp.retrbinary('RETR ftpTemp.txt', gFile.write)
    gFile.close()
    gFile = open("ftpTemp.txt", "r")
    buff = gFile.read()
    gFile.close()
    convertTxtArray = buff.split()
    return float(convertTxtArray[0]), float(convertTxtArray[1])


time_stamp = time.time()
while True:
    if time.time() - time_stamp > 0.1:
        motor1_count_request_new, motor2_count_request_new = updateFTPfile()
        time_stamp = time.time()
    else:
    motor1.move_to_position(int(motor1_count_request_new))
    time.sleep(0.001)
    motor2.move_to_position(int(motor2_count_request_new))
