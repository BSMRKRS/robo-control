try:
    import RPi.GPIO as GPIO
    import armControlSSH
except:
    import armControlTCP
