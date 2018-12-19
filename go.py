import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
def go():
        RPL.servoWrite(4, 2000)
        RPL.servoWrite(3, 1000)
