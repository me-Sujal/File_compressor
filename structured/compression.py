# compression.py
class Compressor:
    def __init__(self, filename):
        self.filename = filename

    def compress(self, encoded_data):
        encoded_data = encoded_data.strip().replace('\n', '')
        padding_length = (8 - len(encoded_data) % 8) % 8
        
        bytes_data = bytearray([padding_length])
        encoded_data += '0' * padding_length

        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            bytes_data.append(int(byte, 2))

        return bytes_data

    def decompress(self, bytes_data):
        padding_length = bytes_data[0]
        bit_string = ''
        
        for byte in bytes_data[1:]:
            bit_string += format(byte, '08b')

        if padding_length > 0:
            bit_string = bit_string[:-padding_length]

        return bit_string
