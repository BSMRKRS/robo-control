try:
    print("Attepting to Establish SSH Connection")
    import RPi.GPIO as GPIO
    import armControlSSH
except:
    print("No SSH Connection")
    print("Attempting to connect TCP with controller")
    import armControlTCP_xbox
