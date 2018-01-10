import math
import xbox



if __name__ == '__main__':
    joy = xbox.Joystick()

    while not joy.Back():


        x, y = joy.leftStick()
        print x
        print y
    joy.close()
