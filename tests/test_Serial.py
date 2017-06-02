from raspibot.Serial import AttinyProtocol


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
    encoder_bytes = left.to_bytes(2, 'little') + right.to_bytes(2, 'little')
    serial = MockSerial(encoder_bytes)
    
    attiny = AttinyProtocol(serial)
    result = attiny.get_encoders()
    
    assert serial.received == b'\x04'
    
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
    encoder_bytes = value.to_bytes(2, 'little')
    serial = MockSerial(encoder_bytes)
    
    attiny = AttinyProtocol(serial)
    result = attiny.get_left_encoder()
    
    assert serial.received == b'\x03'
    assert result == value
    
def test_get_right_encoder():
    value = 21845
    encoder_bytes = value.to_bytes(2, 'little')
    serial = MockSerial(encoder_bytes)
    
    attiny = AttinyProtocol(serial)
    result = attiny.get_right_encoder()
    
    assert serial.received == b'\x02'
    assert result == value
    
# flake8: noqa
