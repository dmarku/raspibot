from raspibot.Serial import AttinyProtocol


class MockSerial:

    def __init__(self, bytes):
        self._bytes = bytes
        self._position = 0

    def write(self, bytes):
        pass

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
    
    # use it as a tuple
    assert result == (left, right)
    
    # access tuple fields by index
    assert result[0] == left
    assert result[1] == right
    
    # access tuple fields by name
    assert result.left == left
    assert result.right == right
    
# flake8: noqa
