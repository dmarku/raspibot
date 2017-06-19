"""Provides a class for controlling the RaspiBot's LCD display."""
import RPi.GPIO as GPIO
from time import sleep


def _bits(byte):
    return [(0 if (byte & (1 << i)) == 0 else 1) for i in reversed(range(8))]


class Display:
    """Implements the communication protocol for the RaspiBot v2's LCD."""

    def __init__(self):
        """Create a display object with default GPIO pin numbers."""
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
        """Initialize the GPIO pins and ensure 4-bit communication mode."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(
            [self.enable, self.rw, self.register_select],
            GPIO.OUT,
            initial=GPIO.LOW)
        GPIO.setup(self.data, GPIO.OUT, initial=GPIO.LOW)

        # initialize to 4-bit mode regardless of initial state
        self._write_nibble([0, 0, 1, 1])
        self._write_nibble([0, 0, 1, 1])
        self._write_nibble([0, 0, 1, 1])
        self._write_nibble([0, 0, 1, 0])

        # initialize entry mode
        self._write_byte([0, 0, 0, 0, 0, 1, 1, 0])

        # initialize display control
        self._write_byte([0, 0, 0, 0, 1, 1, 1, 1])

        # initialize function mode
        self._write_byte([0, 0, 1, 0, 1, 0, 0, 0])

    def _wait_for_controller(self):
        """Stop communication until the previous transfer is complete."""
        # TODO: implement waiting for busy flag
        sleep(0.002)

    def _write_nibble(self, nibble):
        """Send four bits to the display controller."""
        GPIO.output(self.rw, 0)
        GPIO.output(self.enable, 1)
        GPIO.output(self.data, nibble)
        GPIO.output(self.enable, 0)
        self.wait_for_controller()

    def _write_byte(self, bits):
        """Send a whole byte to the display controller."""
        self._write_nibble(bits[0:4])
        self._write_nibble(bits[4:8])

    def _select_data_register(self):
        GPIO.output(self.register_select, 1)

    def _select_instruction_register(self):
        GPIO.output(self.register_select, 0)

    def clear(self):
        """
        Clear display and reset cursor.

        Clear the LCD of any content and reset the cursor to the top left
        character of the display.
        """
        GPIO.output(self.register_select, 0)
        self._write_byte([0, 0, 0, 0, 0, 0, 0, 1])

    def print_codepoint(self, bits):
        """Print a single character at the cursor position."""
        self._select_data_register()
        self._write_byte(bits)

    def cursor_goto_line(self, line):
        """Set the cursor to the beginning of a line."""
        self._select_instruction_register()
        # WARNING: only works as expected for line == 1 or line == 0
        line = 0 if line == 0 else 1
        self._write_byte([1, line, 0, 0, 0, 0, 0, 0])

    def print(self, string):
        """Print a string at the cursor position."""
        # ASCII encoding is probably the closest to the HDS44780's actual
        # encoding
        for c in string.encode('ascii'):
            self.print_codepoint(_bits(c))

    # TODO: figure out a better way to cleanup GPIO instead of letting the
    # user call this manually...
    def cleanup(self):
        """Free any used GPIO pins."""
        GPIO.cleanup(self.data + [self.enable, self.rw, self.register_select])