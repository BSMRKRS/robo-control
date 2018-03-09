try:
    import RPi.GPIO as GPIO
    connection = True
    print "Running on RaspberryPi, operating armControl through SSH"
except:
    connection = False
    print "Not running on RaspberryPi, setting up FTP mode"

if connection:
    import armControlSSH
else:
    import armControlFTP
