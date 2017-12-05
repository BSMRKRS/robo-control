import RPi.GPIO as GPIO
import math
import xbox

GPIO_LED_GREEN  = 23
GPIO_LED_RED    = 22
GPIO_LED_YELLOW = 27
GPIO_LED_BLUE   = 17

GPIO_SERVO_PIN  = 25


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_LED_GREEN, GPIO.OUT)
GPIO.setup(GPIO_LED_RED, GPIO.OUT)
GPIO.setup(GPIO_LED_YELLOW, GPIO.OUT)
GPIO.setup(GPIO_LED_BLUE, GPIO.OUT)
GPIO.setup(GPIO_SERVO_PIN, GPIO.OUT)


def updateServo(pwm, angle):
    duty = float(angle) / 10.0 + 2.5
    pwm.ChangeDutyCycle(duty)

def angleFromCoords(x,y):
    angle = 0.0
    if x==0.0 and y==0.0:
        angle = 90.0
    elif x>=0.0 and y>=0.0:
        # first quadrant
        angle = math.degrees(math.atan(y/x)) if x!=0.0 else 90.0
    elif x<0.0 and y>=0.0:
        # second quadrant
        angle = math.degrees(math.atan(y/x))
        angle += 180.0
    elif x<0.0 and y<0.0:
        # third quadrant
        angle = math.degrees(math.atan(y/x))
        angle += 180.0
    elif x>=0.0 and y<0.0:
        # third quadrant
        angle = math.degrees(math.atan(y/x)) if x!=0.0 else -90.0
        angle += 360.0
    return angle

if __name__ == '__main__':
    joy = xbox.Joystick()
    pwm = GPIO.PWM(GPIO_SERVO_PIN, 100)
    pwm.start(5)

    while not joy.Back():

        # LEDs
        led_state_green  = GPIO.HIGH if joy.A() else GPIO.LOW
        led_state_red    = GPIO.HIGH if joy.B() else GPIO.LOW
        led_state_yellow = GPIO.HIGH if joy.Y() else GPIO.LOW
        led_state_blue   = GPIO.HIGH if joy.X() else GPIO.LOW

        GPIO.output(GPIO_LED_GREEN, led_state_green)
        GPIO.output(GPIO_LED_RED, led_state_red)
        GPIO.output(GPIO_LED_YELLOW, led_state_yellow)
        GPIO.output(GPIO_LED_BLUE, led_state_blue)

        # Servo
        x, y = joy.leftStick()
        angle = angleFromCoords(x,y)
        if angle > 180 and angle < 270:
            angle = 180
        elif angle >= 270:
            angle = 0
        updateServo(pwm, angle)


    joy.close()
    pwm.stop()
