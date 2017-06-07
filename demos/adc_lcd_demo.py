"""
Show sensor readings on the LCD.

Repeatedly read left and right Sharp sensor values from the ADC module and
display them on the LCD.
"""
from smbus import SMBus
from time import sleep
import RPi.GPIO as GPIO

from adc import ADC
from LCD import Display

d = Display()
d.init()

bus_number = 1
bus_address = 0x49

bus = SMBus(bus_number)
a = ADC(bus, bus_address)

left_channel = 0
right_channel = 1

refresh_interval = 0.1

try:
    while True:
        left = a.read_channel(left_channel)
        right = a.read_channel(right_channel)

        d.cursor_goto_line(0)
        d.print_string('L {0:>4d}    R {1:>4d}'.format(left, right))

        sleep(refresh_interval)
except KeyboardInterrupt:
    GPIO.cleanup()
