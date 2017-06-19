# -*- coding: utf-8 -*-

# LCD control for the RaspiBot v2
# basically, an implementation of the HD44780 controller protocol,
# made-to-measure for our 4-bit interface to a 16x2 character LCD

import RPi.GPIO as GPIO
from time import sleep

bits = lambda byte :  [(0 if (byte & (1 << i)) == 0 else 1) for i in reversed(range(8))]

class Display:
    def __init__(self):
        # pin numbers, defaults to BCM GPIO numbering
        self.enable = 27
        self.rw = 18
        self.register_select = 17

        self.d4 = 8
        self.d5 = 7
        self.d6 = 5
        self.d7 = 6

        # define data pins in descending order, so the bits of a nibble can be
        # written in descending order as well, i.e. 0b0011 as
        # GPIO.output(self.data, [0, 0, 1, 1])
        self.data = [self.d7, self.d6, self.d5, self.d4]


    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(
            [self.enable, self.rw, self.register_select],
            GPIO.OUT,
            initial=GPIO.LOW)
        GPIO.setup(self.data, GPIO.OUT, initial=GPIO.LOW)

        # initialize to 4-bit mode regardless of initial state
        self.write_nibble([0, 0, 1, 1])
        self.write_nibble([0, 0, 1, 1])
        self.write_nibble([0, 0, 1, 1])
        self.write_nibble([0, 0, 1, 0])

        # initialize entry mode
        self.write_byte([0, 0, 0, 0, 0, 1, 1, 0])

        # initialize display control
        self.write_byte([0, 0, 0, 0, 1, 1, 1, 1])

        # initialize function mode
        self.write_byte([0, 0, 1, 0, 1, 0, 0, 0])

    def wait_for_controller(self):
        GPIO.output(self.rw, 1)
        GPIO.wait_for_edge(self.d7, GPIO.FALLING)
        

    def write_nibble(self, nibble):
        GPIO.output(self.rw, 0)
        GPIO.output(self.enable, 1)
        GPIO.output(self.data, nibble)
        GPIO.output(self.enable, 0)
        self.wait_for_controller()

    def write_byte(self, bits):
        self.write_nibble(bits[0:4])
        self.write_nibble(bits[4:8])

    def clear(self):
        GPIO.output(self.register_select, 0)
        self.write_byte([0, 0, 0, 0, 0, 0, 0, 1])

    def cursor_off(self):
        GPIO.output(self.register_select, 0)
        self.write_byte([0, 0, 0, 0, 1, 1, 0, 0])

    def cursor_on(self):
        GPIO.output(self.register_select, 0)
        self.write_byte([0, 0, 0, 0, 1, 1, 1, 1])

    def select_data_register(self):
        GPIO.output(self.register_select, 1)

    def select_instruction_register(self):
        GPIO.output(self.register_select, 0)

    def print(self, bits):
        self.select_data_register()
        self.write_byte(bits)

    def print_string(self, string):
        for c in string.encode('ascii'):
            self.print(bits(c))

    def cursor_goto_xy(self, x ,y ):
        self.select_instruction_register()
        # WARNING: only works as expected for line == 1 or line == 0
        y = 0 if y == 0 else 1
        self.write_byte([1, y, x&32, x&16, x&8, x&4, x&2, x&1])

    def load_custom_character(self, picture, number):
        if ((number>=0)&&(number<=7))
            self.write_byte([0, 1, number&4, number&2, number&1, 0, 0, 0])
            for c in range(8):
            self.print(bits(picture[c]))

    # TODO: figure out a better way to cleanup GPIO instead of letting the
    # user call this manually...
    def cleanup(self):
        # TODO: only clean up pins that are actually used
        GPIO.cleanup()
