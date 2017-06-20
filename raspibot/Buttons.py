import RPi.GPIO as GPIO
from time import sleep

class Button(object):
    def __init__(self, pinButtonPress, pinLedRed, pinLedGreen):
        self.LED_RED = pinLedRed
        self.LED_GREEN = pinLedGreen
        self.BUTTON = pinButtonPress
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON, direction=GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup([self.LED_RED, self.LED_GREEN], direction=GPIO.OUT, initial=1)

    def setRedLED(self, toggle): # true or false works as well as 1 or 0. Numbers other than 0 will be interpreted as true
        GPIO.output(self.LED_RED, not toggle)

    def setGreenLED(self, toggle): # true or false works as well as 1 or 0. Numbers other than 0 will be interpreted as true
        GPIO.output(self.LED_GREEN, not toggle)

    def waitForButtonPress(self):
        while not self.isPressed():
            sleep(0.0001)

    def waitForButtonRelease(self):
        while self.isPressed():
            sleep(0.0001)

    def waitForButton(self):
        self.waitForButtonPress()
        self.waitForButtonRelease()

    def isPressed(self):
        if(GPIO.input(self.BUTTON)): return True
        else: return False
