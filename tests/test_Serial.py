from raspibot.Serial import AttinyProtocol, InvalidResponseException, InvalidLengthException

import pytest

ALIVE = b'\x01'

ENCODERS_RIGHT = b'\x02'
ENCODERS_LEFT = b'\x03'
ENCODERS_BOTH = b'\x04'

ENCODERS_RESET_RIGHT = b'\x05'
ENCODERS_RESET_LEFT = b'\x06'
ENCODERS_RESET_BOTH = b'\x07'

ECHO = b'\x0C'

ACK = b'\x10'
NAK = b'\x14'

INVALID_RESPONSE = b'\x23'

STOP_MOTORS = b'\x21'

SET_RIGHT_MOTOR = b'\x25'
SET_LEFT_MOTOR = b'\x29'
SET_BOTH_MOTORS = b'\x2D'

SET_PI = b'\x2F'

MOTOR_MIN = -127
MOTOR_MAX = 127
MOTOR_ZERO = 0

# as signed byte values:
BYTES_MOTOR_MIN = MOTOR_MIN.to_bytes(1, 'big', signed=True)
BYTES_MOTOR_MAX = MOTOR_MAX.to_bytes(1, 'big', signed=True)
BYTES_MOTOR_ZERO = MOTOR_ZERO.to_bytes(1, 'big', signed=True)

class MockSerial:

    def __init__(self, bytes):
        self._bytes = bytes
        self._position = 0
        self.received = b''

    def write(self, bytes):
        self.received += bytes

    def read(self, count):
        try:
            return self._bytes[self._position:self._position+count]
            self._position += count
        except IndexError:
            return b''


def test_get_encoders():
    left, right = 0, 65535
    encoder_bytes = left.to_bytes(2, 'big') + right.to_bytes(2, 'big')
    serial = MockSerial(encoder_bytes)
    
    attiny = AttinyProtocol(serial)
    result = attiny.get_encoders()
    
    assert serial.received == ENCODERS_BOTH
    
    # use it as a tuple
    assert result == (left, right)
    
    # access tuple fields by index
    assert result[0] == left
    assert result[1] == right
    
    # access tuple fields by name
    assert result.left == left
    assert result.right == right
    
def test_get_left_encoder():
    value = 43690
    encoder_bytes = value.to_bytes(2, 'big')
    serial = MockSerial(encoder_bytes)
    
    attiny = AttinyProtocol(serial)
    result = attiny.get_left_encoder()
    
    assert serial.received == ENCODERS_LEFT
    assert result == value
    
def test_get_right_encoder():
    value = 21845
    encoder_bytes = value.to_bytes(2, 'big')
    serial = MockSerial(encoder_bytes)
    
    attiny = AttinyProtocol(serial)
    result = attiny.get_right_encoder()
    
    assert serial.received == ENCODERS_RIGHT
    assert result == value
    
def test_reset_right_encoder():
    serial = MockSerial(ACK)
    attiny = AttinyProtocol(serial)
    
    result = attiny.reset_right_encoder()
    
    assert serial.received == ENCODERS_RESET_RIGHT
    assert result == True
    
def test_reset_right_encoder_nak():
    serial = MockSerial(NAK)
    attiny = AttinyProtocol(serial)
    
    result = attiny.reset_right_encoder()
    
    assert serial.received == ENCODERS_RESET_RIGHT
    assert result == False
    
def test_reset_right_encoder_timeout():
    serial = MockSerial(b'')
    attiny = AttinyProtocol(serial)
    
    result = attiny.reset_right_encoder()
    
    assert serial.received == ENCODERS_RESET_RIGHT
    assert result == False
    
def test_reset_right_encoder_invalid():
    serial = MockSerial(INVALID_RESPONSE)
    attiny = AttinyProtocol(serial)
    
    with pytest.raises(InvalidResponseException):
        attiny.reset_right_encoder()
        
    assert serial.received == ENCODERS_RESET_RIGHT
    
def test_reset_left_encoder():
    serial = MockSerial(ACK)
    attiny = AttinyProtocol(serial)
    
    result = attiny.reset_left_encoder()
    
    assert serial.received == ENCODERS_RESET_LEFT
    assert result == True
    
def test_reset_left_encoder_nak():
    serial = MockSerial(NAK)
    attiny = AttinyProtocol(serial)
    
    result = attiny.reset_left_encoder()
    
    assert serial.received == ENCODERS_RESET_LEFT
    assert result == False
    
def test_reset_left_encoder_timeout():
    serial = MockSerial(b'')
    attiny = AttinyProtocol(serial)
    
    result = attiny.reset_left_encoder()
    
    assert serial.received == ENCODERS_RESET_LEFT
    assert result == False
    
def test_reset_left_encoder_invalid():
    serial = MockSerial(INVALID_RESPONSE)
    attiny = AttinyProtocol(serial)
    
    with pytest.raises(InvalidResponseException):
        attiny.reset_left_encoder()
        
    assert serial.received == ENCODERS_RESET_LEFT
    
def test_reset_both_encoders():
    serial = MockSerial(ACK)
    attiny = AttinyProtocol(serial)
    
    result = attiny.reset_encoders()
    
    assert serial.received == ENCODERS_RESET_BOTH
    assert result == True
    
def test_reset_both_encoders_nak():
    serial = MockSerial(NAK)
    attiny = AttinyProtocol(serial)
    
    result = attiny.reset_encoders()
    
    assert serial.received == ENCODERS_RESET_BOTH
    assert result == False
    
def test_reset_both_encoders_timeout():
    serial = MockSerial(b'')
    attiny = AttinyProtocol(serial)
    
    result = attiny.reset_encoders()
    
    assert serial.received == ENCODERS_RESET_BOTH
    assert result == False
    
def test_reset_both_encoders_invalid():
    serial = MockSerial(INVALID_RESPONSE)
    attiny = AttinyProtocol(serial)
    
    with pytest.raises(InvalidResponseException):
        attiny.reset_encoders()
        
    assert serial.received == ENCODERS_RESET_BOTH
    
def test_alive_ack():
    # send out an ACK byte
    serial = MockSerial(ACK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.alive()
    
    assert serial.received == ALIVE
    assert result == True
    
def test_alive_nak():
    # send out an NAK byte
    serial = MockSerial(NAK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.alive()
    
    assert serial.received == ALIVE
    assert result == False
    
def test_alive_undefined():
    # send out something that is neither an ACK or a NAK byte
    serial = MockSerial(INVALID_RESPONSE)
    
    attiny = AttinyProtocol(serial)
    with pytest.raises(InvalidResponseException):
        attiny.alive()

    assert serial.received == ALIVE
    
ECHO_TEST = b'\x88'
# a byte that is not ECHO_TEST
ECHO_INVALID = b'\x44'

def test_echo():
    serial = MockSerial(ECHO_TEST)
    
    attiny = AttinyProtocol(serial)
    
    response = attiny.echo(ECHO_TEST)
    
    assert serial.received == ECHO + ECHO_TEST
    assert response == ECHO_TEST

def test_echo_too_long():
    serial = MockSerial(b'')
    
    attiny = AttinyProtocol(serial)
    
    with pytest.raises(InvalidLengthException):
        attiny.echo(b'abcd')
        
    assert serial.received == b''

def test_echo_invalid():
    serial = MockSerial(ECHO_INVALID)
    
    attiny = AttinyProtocol(serial)
    
    with pytest.raises(InvalidResponseException):
        attiny.echo(ECHO_TEST)
    
    assert serial.received == ECHO + ECHO_TEST
    
def test_stop_motors():
    serial = MockSerial(ACK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.stop_motors()
    
    assert serial.received == STOP_MOTORS
    
    assert result == True
    
def test_stop_motors_nak():
    serial = MockSerial(NAK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.stop_motors()
    
    assert serial.received == STOP_MOTORS
    
    assert result == False
    
def test_stop_motors_timeout():
    serial = MockSerial(b'')
    
    attiny = AttinyProtocol(serial)
    result = attiny.stop_motors()
    
    assert serial.received == STOP_MOTORS
    
    assert result == False
    
def test_stop_motors_undefined():
    # send out something that is neither an ACK or a NAK byte
    serial = MockSerial(INVALID_RESPONSE)
    
    attiny = AttinyProtocol(serial)
    with pytest.raises(InvalidResponseException):
        attiny.stop_motors()

    assert serial.received == STOP_MOTORS

def test_set_right_motor_min():
    serial = MockSerial(ACK)
    
    right = MOTOR_MIN
    right_bytes = BYTES_MOTOR_MIN
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_right_motor(right)
    
    assert len(serial.received) == 2
    assert serial.received == SET_RIGHT_MOTOR + right_bytes
    
    assert result == True

def test_set_right_motor_under_min():
    serial = MockSerial(ACK)
    
    right = MOTOR_MIN - 1
    right_bytes = BYTES_MOTOR_MIN
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_right_motor(right)
    
    assert len(serial.received) == 2
    assert serial.received == SET_RIGHT_MOTOR + right_bytes
    
    assert result == True

def test_set_right_motor_max():
    serial = MockSerial(ACK)
    
    right = MOTOR_MAX
    right_bytes = BYTES_MOTOR_MAX
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_right_motor(right)
    
    assert len(serial.received) == 2
    assert serial.received == SET_RIGHT_MOTOR + right_bytes
    
    assert result == True

def test_set_right_motor_over_max():
    serial = MockSerial(ACK)
    
    right = MOTOR_MAX + 1
    right_bytes = BYTES_MOTOR_MAX
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_right_motor(right)
    
    assert len(serial.received) == 2
    assert serial.received == SET_RIGHT_MOTOR + right_bytes
    
    assert result == True

def test_set_right_motor_zero():
    serial = MockSerial(ACK)
    
    right = MOTOR_ZERO
    right_bytes = BYTES_MOTOR_ZERO
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_right_motor(right)
    
    assert len(serial.received) == 2
    assert serial.received == SET_RIGHT_MOTOR + right_bytes
    
    assert result == True

def test_set_right_motor_nak():
    serial = MockSerial(NAK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_right_motor(0)
    
    assert result == False

def test_set_right_motor_timeout():
    serial = MockSerial(b'')
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_right_motor(0)
    
    assert result == False

def test_set_right_motor_invalid():
    serial = MockSerial(INVALID_RESPONSE)
    
    attiny = AttinyProtocol(serial)
    with pytest.raises(InvalidResponseException):
        attiny.set_right_motor(0)
        
    assert serial.received[:1] == SET_RIGHT_MOTOR
    

def test_set_left_motor_min():
    serial = MockSerial(ACK)
    
    left = MOTOR_MIN
    left_bytes = BYTES_MOTOR_MIN
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_left_motor(left);
    
    assert len(serial.received) == 2
    assert serial.received == SET_LEFT_MOTOR + left_bytes
    
    assert result == True

def test_set_left_motor_under_min():
    serial = MockSerial(ACK)
    
    left = MOTOR_MIN - 1
    left_bytes = BYTES_MOTOR_MIN
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_left_motor(left);
    
    assert len(serial.received) == 2
    assert serial.received == SET_LEFT_MOTOR + left_bytes
    
    assert result == True

def test_set_left_motor_max():
    serial = MockSerial(ACK)
    
    left = MOTOR_MAX
    left_bytes = BYTES_MOTOR_MAX
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_left_motor(left);
    
    assert len(serial.received) == 2
    assert serial.received == SET_LEFT_MOTOR + left_bytes
    
    assert result == True

def test_set_left_motor_over_max():
    serial = MockSerial(ACK)
    
    left = MOTOR_MAX + 1
    left_bytes = BYTES_MOTOR_MAX
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_left_motor(left);
    
    assert len(serial.received) == 2
    assert serial.received == SET_LEFT_MOTOR + left_bytes
    
    assert result == True


def test_set_left_motor_zero():
    serial = MockSerial(ACK)
    
    left = MOTOR_ZERO
    left_bytes = BYTES_MOTOR_ZERO
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_left_motor(left);
    
    assert len(serial.received) == 2
    assert serial.received == SET_LEFT_MOTOR + left_bytes
    
    assert result == True


def test_set_left_motor_nak():
    serial = MockSerial(NAK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_left_motor(0)
    
    assert result == False


def test_set_left_motor_timeout():
    serial = MockSerial(b'')
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_left_motor(0)
    
    assert result == False


def test_set_left_motor_invalid():
    serial = MockSerial(INVALID_RESPONSE)
    
    attiny = AttinyProtocol(serial)
    with pytest.raises(InvalidResponseException):
        attiny.set_left_motor(0)
        
    assert serial.received[:1] == SET_LEFT_MOTOR

def test_set_both_motors_minmax():
    serial = MockSerial(ACK)
    
    left = MOTOR_MIN
    left_bytes = BYTES_MOTOR_MIN
    
    right = MOTOR_MAX
    right_bytes = BYTES_MOTOR_MAX
    
    attiny = AttinyProtocol(serial)
    attiny.set_motors(left, right)
    
    assert len(serial.received) == 3
    assert serial.received == SET_BOTH_MOTORS + left_bytes + right_bytes
    
def test_set_both_motors_exceed_minmax():
    serial = MockSerial(ACK)
    
    left = MOTOR_MIN - 1
    left_bytes = BYTES_MOTOR_MIN
    
    right = MOTOR_MAX + 1
    right_bytes = BYTES_MOTOR_MAX
    
    attiny = AttinyProtocol(serial)
    attiny.set_motors(left, right)
    
    assert len(serial.received) == 3
    assert serial.received == SET_BOTH_MOTORS + left_bytes + right_bytes
    
def test_set_both_motors_maxmin():
    serial = MockSerial(ACK)
    
    left = MOTOR_MAX
    left_bytes = BYTES_MOTOR_MAX
    
    right = MOTOR_MIN
    right_bytes = BYTES_MOTOR_MIN
    
    attiny = AttinyProtocol(serial)
    attiny.set_motors(left, right)
    
    assert len(serial.received) == 3
    assert serial.received == SET_BOTH_MOTORS + left_bytes + right_bytes
    
def test_set_both_motors_exceed_maxmin():
    serial = MockSerial(ACK)
    
    left = MOTOR_MAX + 1
    left_bytes = BYTES_MOTOR_MAX
    
    right = MOTOR_MIN - 1
    right_bytes = BYTES_MOTOR_MIN
    
    attiny = AttinyProtocol(serial)
    attiny.set_motors(left, right)
    
    assert len(serial.received) == 3
    assert serial.received == SET_BOTH_MOTORS + left_bytes + right_bytes
    
def test_set_both_motors_zero():
    serial = MockSerial(ACK)
    
    left = MOTOR_ZERO
    left_bytes = BYTES_MOTOR_ZERO
    
    right = MOTOR_ZERO
    right_bytes = BYTES_MOTOR_ZERO
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_motors(left, right)
    
    assert len(serial.received) == 3
    assert serial.received == SET_BOTH_MOTORS + left_bytes + right_bytes
    
    assert result == True
    
def test_set_both_motors_nak():
    serial = MockSerial(NAK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_motors(0, 0)
    
    assert result == False
    
def test_set_both_motors_timeout():
    serial = MockSerial(b'')
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_motors(0, 0)
    
    assert result == False
    
def test_set_both_motors_invalid():
    serial = MockSerial(INVALID_RESPONSE)
    
    attiny = AttinyProtocol(serial)
    with pytest.raises(InvalidResponseException):
        attiny.set_motors(0, 0)
        
    assert serial.received[:1] == SET_BOTH_MOTORS

INT16_MIN = -(2 ** 16 // 2)
INT16_MAX = 2 ** 16 // 2 - 1
UINT8_MIN = 0
UINT8_MAX = 2 ** 8 - 1

INT16_MIN_ENCODED = INT16_MIN.to_bytes(2, 'big', signed=True)
INT16_MAX_ENCODED = INT16_MAX.to_bytes(2, 'big', signed=True)
UINT8_MIN_ENCODED = UINT8_MIN.to_bytes(1, 'big')
UINT8_MAX_ENCODED = UINT8_MAX.to_bytes(1, 'big')

def test_set_pi_parameters_min():
    serial = MockSerial(ACK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_pi_parameters(INT16_MIN, INT16_MIN, UINT8_MIN)
    
    assert result == True
    
    assert len(serial.received) == 6
    assert serial.received[:1] == SET_PI
    assert serial.received[1:3] == INT16_MIN_ENCODED
    assert serial.received[3:5] == INT16_MIN_ENCODED
    assert serial.received[5:] == UINT8_MIN_ENCODED
    
def test_set_pi_parameters_under_min():
    serial = MockSerial(ACK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_pi_parameters(INT16_MIN - 1, INT16_MIN - 1, UINT8_MIN - 1)
    
    assert result == True
    
    assert len(serial.received) == 6
    assert serial.received[:1] == SET_PI
    assert serial.received[1:3] == INT16_MIN_ENCODED
    assert serial.received[3:5] == INT16_MIN_ENCODED
    assert serial.received[5:] == UINT8_MIN_ENCODED
    
def test_set_pi_parameters_max():
    serial = MockSerial(ACK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_pi_parameters(INT16_MAX, INT16_MAX, UINT8_MAX)
    
    assert result == True
    
    assert len(serial.received) == 6
    assert serial.received[:1] == SET_PI
    assert serial.received[1:3] == INT16_MAX_ENCODED
    assert serial.received[3:5] == INT16_MAX_ENCODED
    assert serial.received[5:] == UINT8_MAX_ENCODED
    
def test_set_pi_parameters_over_max():
    serial = MockSerial(ACK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_pi_parameters(INT16_MAX + 1, INT16_MAX + 1, UINT8_MAX + 1)
    
    assert result == True
    
    assert len(serial.received) == 6
    assert serial.received[:1] == SET_PI
    assert serial.received[1:3] == INT16_MAX_ENCODED
    assert serial.received[3:5] == INT16_MAX_ENCODED
    assert serial.received[5:] == UINT8_MAX_ENCODED
    
def test_set_pi_parameters_inrange():
    p = 0
    i = -1
    s = 1
    
    p_encoded = p.to_bytes(2, 'big', signed=True)
    i_encoded = i.to_bytes(2, 'big', signed=True)
    s_encoded = s.to_bytes(1, 'big')
    
    serial = MockSerial(ACK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_pi_parameters(p, i, s)
    
    assert result == True
    
    assert len(serial.received) == 6
    assert serial.received[:1] == SET_PI
    assert serial.received[1:3] == p_encoded
    assert serial.received[3:5] == i_encoded
    assert serial.received[5:] == s_encoded
    
def test_set_pi_parameters_nak():
    serial = MockSerial(NAK)
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_pi_parameters(0, 0, 0)
    
    assert len(serial.received) == 6
    assert result == False
    
def test_set_pi_parameters_timeout():
    serial = MockSerial(b'')
    
    attiny = AttinyProtocol(serial)
    result = attiny.set_pi_parameters(0, 0, 0)
    
    assert len(serial.received) == 6
    assert result == False
    
def test_set_pi_parameters_timeout():
    serial = MockSerial(INVALID_RESPONSE)
    
    attiny = AttinyProtocol(serial)
    
    with pytest.raises(InvalidResponseException):
        attiny.set_pi_parameters(0, 0, 0)

    assert len(serial.received) == 6
    assert serial.received[:1] == SET_PI
    
# flake8: noqa
