# --------------------------------File on client--------------------------------
# Reads

import RoboPiLib as RPL
import ftplib
while True:
    ftp = ftplib.FTP('ip', 'username', 'password')
    ftp.cwd('Desktop/Robot-Controller-Support')
    gFile = open("ftpTemp", "wb")
    ftp.retrbinary('RETR ftptestFile.txt', gFile.write)
    gFile.close()
    ftp.quit()
    gFile = open("ftpTemp", "r")
    buff = gFile.read()
    convertTxtArray = buff.split()
    motorL = convertTxtArray[0]
    motorR = convertTxtArray[1]
    RPL.servoWrite(0, int(float(motorL))) # for some odd reason would not convert directly to int with int()
    RPL.servoWrite(1, int(float(motorR))) # for some odd reason would not convert directly to int with int()
