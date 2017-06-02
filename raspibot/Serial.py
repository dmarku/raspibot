"""Implements the serial interface protocol of RaspiBot's Attiny firmware."""

from collections import namedtuple

EncoderValues = namedtuple('EncoderValues', 'left right')

# Named byte values for the protocol commands
ENCODERS_BOTH = b'\x04'
ENCODERS_LEFT = b'\x03'
ENCODERS_RIGHT = b'\x02'


class AttinyProtocol(object):
    """Provides methods for protocol transactions."""

    def __init__(self, serial):
        """Create a protocol instance on a serial interface."""
        super(AttinyProtocol, self).__init__()
        self._serial = serial

    def get_encoders(self):
        """Request both left and right encoder values."""
        self._serial.write(ENCODERS_BOTH)
        response = self._serial.read(4)
        left = int.from_bytes(response[:2], 'little')
        right = int.from_bytes(response[2:], 'little')
        return EncoderValues(left, right)

    def get_left_encoder(self):
        """Request the left encoder value."""
        self._serial.write(ENCODERS_LEFT)
        response = self._serial.read(2)
        value = int.from_bytes(response, 'little')
        return value

    def get_right_encoder(self):
        """Request the right encoder value."""
        self._serial.write(ENCODERS_RIGHT)
        response = self._serial.read(2)
        value = int.from_bytes(response, 'little')
        return value
