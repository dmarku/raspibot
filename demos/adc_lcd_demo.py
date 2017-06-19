from smbus import SMBus
from LCD import Display
from raspibot import ADS1015 as ADC
from time import sleep

d = Display()
d.init()

bus_number = 1
bus_address = 0x49

bus = SMBus(bus_number)
a = ADC(bus, bus_address)

left_channel = 0
right_channel = 3

refresh_interval = 0.1

try:
    while True:
        left, right = a.read_channel(left_channel), a.read_channel(right_channel)
        d.cursor_goto_line(0)
        d.print_string('L {0:>4d}    R {0:>4d}'.format(left, right))
        sleep(refresh_interval)
        
except KeyboardInterrupt:
    pass
