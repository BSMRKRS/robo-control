# --------------------------------File on client--------------------------------
# Reads

import ArmControlLib as ACL
import ftplib
ftp = ftplib.FTP('ip', 'username', 'password')  # host computer info
ftp.cwd('directory of this repository')  # directory of repo on host

## Motor 1 ##
motor1 = ACL.Motor(0, 1, 26, 20, 1000, 1000, 21848.88, freq)


## Motor2 ##
motor2 = ACL.Motor(2, 3, 19, 16, 1000, 1000, 11098.56, freq)


while True:
    gFile = open("ftpTemp.txt", "wb")
    ftp.retrbinary('RETR ftpTemp', gFile.write)
    gFile.close()
    ftp.quit()
    gFile = open("ftpTemp.txt", "r")
    buff = gFile.read()
    convertTxtArray = buff.split()
    motor1_count_request = convertTxtArray[0]
    motor2_count_request = convertTxtArray[1]
    latency = time.time() - float(convertTxtArray[2])
    motor1.move_to_position(motor1_count_request)
    motor2.move_to_position(motor2_count_request)
    print latency
