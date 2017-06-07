"""Read sharp sensor values and log them to the console."""

from smbus import SMBus
from time import sleep
import RPi.GPIO as GPIO

from adc import ADC

bus_number = 1
bus_address = 0x49

bus = SMBus(bus_number)
adc = ADC(bus, bus_address)

left_channel = 0
right_channel = 1

refresh_interval = 0.1

# Kontinuierliche Ausgabe der Sensorwerte auf der Standardausgabe, bis das
# Programm mit Strg+C beendet wird
try:
    while True:
        left = adc.read_channel(left_channel)
        right = adc.read_channel(right_channel)

        print('L {0:>4d}    R {1:>4d}'.format(left, right))

        sleep(refresh_interval)
except KeyboardInterrupt:
    GPIO.cleanup()
    print('Bye')
