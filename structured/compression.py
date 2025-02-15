# compression.py
class Compressor:
    def __init__(self, filename):
        self.filename = filename

    def compress(self, encoded_data, huffman_codes):
        bytes_data = bytearray()
        
        # Store number of codes (2 bytes)
        bytes_data.extend(len(huffman_codes).to_bytes(2, 'big'))
        
        # Store Huffman codes
        for symbol, code in huffman_codes.items():
            # Convert symbol to int if it's a character
            if isinstance(symbol, str):
                symbol = ord(symbol)
            
            # Store symbol
            bytes_data.append(symbol)
            # Store code length
            bytes_data.append(len(code))
            # Store code bits
            code_int = int(code, 2)
            code_bytes = ((len(code) + 7) // 8)  # Number of bytes needed
            bytes_data.extend(code_int.to_bytes(code_bytes, 'big'))
        
        # Store the actual compressed data
        data_bits = encoded_data.strip().replace('\n', '')
        padding_length = (8 - len(data_bits) % 8) % 8
        
        # Store padding length
        bytes_data.append(padding_length)
        
        # Convert bit string to bytes
        current_byte = 0
        bit_count = 0
        
        for bit in data_bits:
            current_byte = (current_byte << 1) | (int(bit))
            bit_count += 1
            
            if bit_count == 8:
                bytes_data.append(current_byte)
                current_byte = 0
                bit_count = 0
        
        # Handle remaining bits
        if bit_count > 0:
            current_byte = current_byte << (8 - bit_count)
            bytes_data.append(current_byte)

        return bytes_data

    def decompress(self, bytes_data):
        # Read number of codes
        num_codes = int.from_bytes(bytes_data[0:2], 'big')
        
        # Read Huffman codes
        current_pos = 2
        huffman_codes = {}
        
        for _ in range(num_codes):
            symbol = bytes_data[current_pos]
            code_length = bytes_data[current_pos + 1]
            code_bytes = ((code_length + 7) // 8)  # Number of bytes needed
            code_int = int.from_bytes(bytes_data[current_pos + 2:current_pos + 2 + code_bytes], 'big')
            code = format(code_int, f'0{code_length}b')
            # Convert symbol back to character if it's in ASCII range
            if 0 <= symbol <= 127:
                symbol = chr(symbol)
            huffman_codes[symbol] = code
            current_pos += 2 + code_bytes
        
        # Read padding length
        padding_length = bytes_data[current_pos]
        current_pos += 1
        
        # Read compressed data
        bit_string = ''
        for byte in bytes_data[current_pos:-1]:
            bit_string += format(byte, '08b')
        
        # Handle last byte with padding
        if padding_length > 0:
            last_byte = bytes_data[-1]
            bit_string += format(last_byte, '08b')[:-padding_length]
        
        return bit_string, huffman_codes
