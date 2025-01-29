import os

class Compressor:
    def __init__(self, file):
        self.filename = os.path.splitext(file.name)[0] + "_compressedData.bin"

    def compress(self, encoded_huff):
        output_file = self.filename        
        encoded_huff = encoded_huff.strip().replace('\n', '')
        padding_length = (8-len(encoded_huff) % 8) % 8
        
        bytes_data = bytearray([padding_length])

        encoded_huff += '0' * padding_length

        for i in range(0, len(encoded_huff), 8):
            byte = encoded_huff[i:i+8]
            bytes_data.append(int(byte, 2))

        with open(output_file, 'wb') as f:
            f.write(bytes_data)

    def decompress(self, input_file):
        input_file = self.filename
        try:
            with open(input_file, "rb") as file:
                data = file.read()

            padding_length = data[0]

            bit_string = ''
            for byte in data[1:]:
                bit_string += format(byte, '08b')

            if  padding_length > 0:
                bit_string = bit_string[:-padding_length]

            return bit_string

        except FileNotFoundError:
            print("No corresponding *_compressedData file found")

        except IOError:
            print("Error reading the file")

        except Exception as e:
            print(f"{e} has occured")



