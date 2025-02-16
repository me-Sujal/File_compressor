# compression.py
class Compressor:
    def __init__(self, filename):
        self.filename = filename

    def compress(self, encoded_data, huffman_codes):
        bytes_data = bytearray()
        
        # Store number of codes (2 bytes)
        bytes_data.extend(len(huffman_codes).to_bytes(2, 'big'))
        
        # Store Huffman codes
        for symbol, code in sorted(huffman_codes.items()):
            # Store symbol
            if isinstance(symbol, str):
                symbol_value = ord(symbol)
            else:
                symbol_value = symbol
            bytes_data.append(symbol_value)
            
            # Store code length
            code_length = len(code)
            bytes_data.append(code_length)
            
            # Store code as bits
            code_int = int(code, 2)
            bytes_needed = (code_length + 7) // 8
            bytes_data.extend(code_int.to_bytes(bytes_needed, 'big'))
        
        # Store encoded data
        data_bits = encoded_data
        padding_length = (8 - len(data_bits) % 8) % 8
        
        # Store padding length
        bytes_data.append(padding_length)
        
        # Add padding to data bits
        data_bits += '0' * padding_length
        
        # Convert bits to bytes
        for i in range(0, len(data_bits), 8):
            byte_bits = data_bits[i:i+8]
            bytes_data.append(int(byte_bits, 2))
            
        return bytes_data

    def decompress(self, bytes_data):
        # Read number of codes
        num_codes = int.from_bytes(bytes_data[0:2], 'big')
        current_pos = 2
        
        # Read Huffman codes
        huffman_codes = {}
        for _ in range(num_codes):
            # Read symbol
            symbol_value = bytes_data[current_pos]
            symbol = chr(symbol_value) if 0 <= symbol_value <= 127 else symbol_value
            current_pos += 1
            
            # Read code length
            code_length = bytes_data[current_pos]
            current_pos += 1
            
            # Read code
            bytes_needed = (code_length + 7) // 8
            code_int = int.from_bytes(bytes_data[current_pos:current_pos + bytes_needed], 'big')
            code = format(code_int, f'0{code_length}b')[-code_length:]
            current_pos += bytes_needed
            
            huffman_codes[symbol] = code
        
        # Read padding length
        padding_length = bytes_data[current_pos]
        current_pos += 1
        
        # Read encoded data
        bit_string = ''
        for byte in bytes_data[current_pos:]:
            bit_string += format(byte, '08b')
            
        # Remove padding
        if padding_length > 0:
            bit_string = bit_string[:-padding_length]
            
        return bit_string, huffman_codes