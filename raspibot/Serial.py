"""Implements the serial interface protocol of RaspiBot's Attiny firmware."""

from collections import namedtuple

EncoderValues = namedtuple('EncoderValues', 'left right')

# Named byte values for the protocol commands

# Requests
ALIVE = b'\x01'

ENCODERS_RIGHT = b'\x02'
ENCODERS_LEFT = b'\x03'
ENCODERS_BOTH = b'\x04'

ENCODERS_RESET_RIGHT = b'\x05'
ENCODERS_RESET_LEFT = b'\x06'
ENCODERS_RESET_BOTH = b'\x07'

SET_LEFT_MOTOR = b'\x29'
SET_RIGHT_MOTOR = b'\x25'
SET_BOTH_MOTORS = b'\x2D'
STOP_MOTORS = b'\x21'

# Responses
ACK = b'\x10'
NAK = b'\x14'

MOTOR_MIN = -127
MOTOR_MAX = 127


def _clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))


class InvalidResponseException(Exception):
    """
    Raised when the protocol implementation reads an unexpected byte.

    This is typically something that is neither an ACK nor a NAK.
    """

    pass


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
        left = int.from_bytes(response[:2], 'big')
        right = int.from_bytes(response[2:], 'big')
        return EncoderValues(left, right)

    def get_left_encoder(self):
        """Request the left encoder value."""
        self._serial.write(ENCODERS_LEFT)
        response = self._serial.read(2)
        value = int.from_bytes(response, 'big')
        return value

    def get_right_encoder(self):
        """Request the right encoder value."""
        self._serial.write(ENCODERS_RIGHT)
        response = self._serial.read(2)
        value = int.from_bytes(response, 'big')
        return value

    def reset_encoders(self):
        """Request an 'alive' signal from the microcontroller."""
        self._serial.write(ENCODERS_RESET_BOTH)
        response = self._serial.read(1)
        if response == ACK:
            return True
        # empty response can happen on a timeout, which we interpret as
        # "not alive"
        elif response == NAK or response == b'':
            return False
        else:
            raise InvalidResponseException()

    def reset_left_encoder(self):
        """Request an 'alive' signal from the microcontroller."""
        self._serial.write(ENCODERS_RESET_LEFT)
        response = self._serial.read(1)
        if response == ACK:
            return True
        # empty response can happen on a timeout, which we interpret as
        # "not alive"
        elif response == NAK or response == b'':
            return False
        else:
            raise InvalidResponseException()

    def reset_right_encoder(self):
        """Request an 'alive' signal from the microcontroller."""
        self._serial.write(ENCODERS_RESET_RIGHT)
        response = self._serial.read(1)
        if response == ACK:
            return True
        # empty response can happen on a timeout, which we interpret as
        # "not alive"
        elif response == NAK or response == b'':
            return False
        else:
            raise InvalidResponseException()

    def alive(self):
        """Request an 'alive' signal from the microcontroller."""
        self._serial.write(ALIVE)
        response = self._serial.read(1)
        if response == ACK:
            return True
        # empty response can happen on a timeout, which we interpret as
        # "not alive"
        elif response == NAK or response == b'':
            return False
        else:
            raise InvalidResponseException()

    def set_motors(self, left, right):
        """
        Set the speed of both motors.

        Values can be in the range [-127, 127]. Speeds higher than that will be
        set to their respective extreme. Negative values turn the wheel
        backwards, positive values turn it forwards. Zero stops the motor.
        Higher absolute values mean higher speed.
        """
        left = _clamp(left, MOTOR_MIN, MOTOR_MAX)
        right = _clamp(right, MOTOR_MIN, MOTOR_MAX)
        left_bytes = left.to_bytes(1, 'big', signed=True)
        right_bytes = right.to_bytes(1, 'big', signed=True)

        self._serial.write(SET_BOTH_MOTORS + left_bytes + right_bytes)

        response = self._serial.read(1)
        if response == ACK:
            return True
        elif response == NAK or response == b'':
            return False
        else:
            raise InvalidResponseException()

    def set_left_motor(self, speed):
        """
        Set the speed of the left motor.

        Values can be in the range [-127, 127]. Speeds higher than that will be
        set to their respective extreme. Negative values turn the wheel
        backwards, positive values turn it forwards. Zero stops the motor.
        Higher absolute values mean higher speed.
        """
        speed = _clamp(speed, MOTOR_MIN, MOTOR_MAX)
        speed_bytes = speed.to_bytes(1, 'big', signed=True)

        self._serial.write(SET_LEFT_MOTOR + speed_bytes)

        response = self._serial.read(1)
        if response == ACK:
            return True
        elif response == NAK or response == b'':
            return False
        else:
            raise InvalidResponseException()

    def set_right_motor(self, speed):
        """
        Set the speed of the right motor.

        Values can be in the range [-127, 127]. Speeds higher than that will be
        set to their respective extreme. Negative values turn the wheel
        backwards, positive values turn it forwards. Zero stops the motor.
        Higher absolute values mean higher speed.
        """
        speed = _clamp(speed, MOTOR_MIN, MOTOR_MAX)
        speed_bytes = speed.to_bytes(1, 'big', signed=True)

        self._serial.write(SET_RIGHT_MOTOR + speed_bytes)

        response = self._serial.read(1)
        if response == ACK:
            return True
        elif response == NAK or response == b'':
            return False
        else:
            raise InvalidResponseException()
