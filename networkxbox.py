
import math
import ftplib
import sys, tty

""" Xbox 360 controller support for Python
11/9/13 - Steven Jacobs

This class module supports reading a connected xbox controller.
It requires that xboxdrv be installed first:

    sudo apt-get install xboxdrv

See http://pingus.seul.org/~grumbel/xboxdrv/ for details on xboxdrv

Example usage:

    import xbox
    joy = xbox.Joystick()         #Initialize joystick

    if joy.A():                   #Test state of the A button (1=pressed, 0=not pressed)
        print 'A button pressed'
    x_axis   = joy.leftX()        #X-axis of the left stick (values -1.0 to 1.0)
    (x,y)    = joy.leftStick()    #Returns tuple containing left X and Y axes (values -1.0 to 1.0)
    trigger  = joy.rightTrigger() #Right trigger position (values 0 to 1.0)

    joy.close()                   #Cleanup before exit
"""

import subprocess
import os
import select
import time

class Joystick:

    """Initializes the joystick/wireless receiver, launching 'xboxdrv' as a subprocess
    and checking that the wired joystick or wireless receiver is attached.
    The refreshRate determines the maximnum rate at which events are polled from xboxdrv.
    Calling any of the Joystick methods will cause a refresh to occur, if refreshTime has elapsed.
    Routinely call a Joystick method, at least once per second, to avoid overfilling the event buffer.

    Usage:
        joy = xbox.Joystick()
    """
    def __init__(self,refreshRate = 30):
        self.proc = subprocess.Popen(['xboxdrv','--no-uinput','--detach-kernel-driver'], stdout=subprocess.PIPE)
        self.pipe = self.proc.stdout
        #
        self.connectStatus = False  #will be set to True once controller is detected and stays on
        self.reading = '0' * 140    #initialize stick readings to all zeros
        #
        self.refreshTime = 0    #absolute time when next refresh (read results from xboxdrv stdout pipe) is to occur
        self.refreshDelay = 1.0 / refreshRate   #joystick refresh is to be performed 30 times per sec by default
        #
        # Read responses from 'xboxdrv' for upto 2 seconds, looking for controller/receiver to respond
        found = False
        waitTime = time.time() + 2
        while waitTime > time.time() and not found:
            readable, writeable, exception = select.select([self.pipe],[],[],0)
            if readable:
                response = self.pipe.readline()
                # Hard fail if we see this, so force an error
                if response[0:7] == 'No Xbox':
                    raise IOError('No Xbox controller/receiver found')
                # Success if we see the following
                if response[0:12] == 'Press Ctrl-c':
                    found = True
                # If we see 140 char line, we are seeing valid input
                if len(response) == 140:
                    found = True
                    self.connectStatus = True
                    self.reading = response
        # if the controller wasn't found, then halt
        if not found:
            self.close()
            raise IOError('Unable to detect Xbox controller/receiver - Run python as sudo')

    """Used by all Joystick methods to read the most recent events from xboxdrv.
    The refreshRate determines the maximum frequency with which events are checked.
    If a valid event response is found, then the controller is flagged as 'connected'.
    """
    def refresh(self):
        # Refresh the joystick readings based on regular defined freq
        if self.refreshTime < time.time():
            self.refreshTime = time.time() + self.refreshDelay  #set next refresh time
            # If there is text available to read from xboxdrv, then read it.
            readable, writeable, exception = select.select([self.pipe],[],[],0)
            if readable:
                # Read every line that is availabe.  We only need to decode the last one.
                while readable:
                    response = self.pipe.readline()
                    # A zero length response means controller has been unplugged.
                    if len(response) == 0:
                        raise IOError('Xbox controller disconnected from USB')
                    readable, writeable, exception = select.select([self.pipe],[],[],0)
                # Valid controller response will be 140 chars.
                if len(response) == 140:
                    self.connectStatus = True
                    self.reading = response
                else:  #Any other response means we have lost wireless or controller battery
                    self.connectStatus = False
            self.refresh()

    """Return a status of True, when the controller is actively connected.
    Either loss of wireless signal or controller powering off will break connection.  The
    controller inputs will stop updating, so the last readings will remain in effect.  It is
    good practice to only act upon inputs if the controller is connected.  For instance, for
    a robot, stop all motors if "not connected()".

    An inital controller input, stick movement or button press, may be required before the connection
    status goes True.  If a connection is lost, the connection will resume automatically when the
    fault is corrected.
    """
    def connected(self):
        self.refresh()
        return self.connectStatus

    def networkUpdate(self):
        self.refresh()
        response = self.reading()
        file_object = open("xboxCurrentStatusServer.txt","w")
        file_object.truncate()
        file_object.write(response)
        file_object.close()
# Cleanup by ending the xboxdrv subprocess
    def close(self):
        os.system('pkill xboxdrv')
    
