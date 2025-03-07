from core.huffman_codec import HuffmanCodec
from utils.file_handler import FileHandler
from compression import Compressor
import os
import sys

def write_huffman_codes(codes, filename="huffman_codes.txt"):
    with open(filename, 'w') as f:
        for char, code in sorted(codes.items()):
            if isinstance(char, int):
                f.write(f"Value {char} -> {code}\n")
            elif isinstance(char, str) and (char.isspace() or len(char) == 1):
                f.write(f"ASCII {ord(char)}: {char!r} -> {code}\n")
            else:
                f.write(f"Value {char} -> {code}\n")

def process_file(input_path):
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found!")
        return
    
    base_filename = os.path.splitext(input_path)[0]
    try:
        # Initialize codec and compressor
        codec = HuffmanCodec()
        compressor = Compressor(base_filename + "_compressed.bin")
        
        print("Reading input file...")
        data = FileHandler.read_text(input_path)
        
        print("Encoding data...")
        encoded_data = codec.encode(data)
        
        print("Compressing encoded data...")
        compressed_data = compressor.compress(encoded_data, codec.codes)
        print(type(compressed_data))
        
        # Save compressed data
        print(f"Saving compressed data to: {compressor.filename}")
        FileHandler.write_binary(compressor.filename, compressed_data)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e

def decompress_file(compressed_file_path):
    if not os.path.exists(compressed_file_path):
        print(f"Error: File '{compressed_file_path}' not found!")
        return
    
    try:
        # Read the compressed binary file
        print("Reading compressed file...")
        with open(compressed_file_path, 'rb') as f:
            compressed_data = f.read()
        
        # Create compressor instance
        compressor = Compressor(compressed_file_path)
        
        # Get the base filename without "_compressed.bin"
        base_filename = compressed_file_path.replace("_compressed.bin", "")
        
        # Decompress the data
        print("Decompressing data...")
        bit_string, recovered_codes = compressor.decompress(compressed_data)
        
        # Create a new HuffmanCodec instance and set its codes
        codec = HuffmanCodec()
        codec.set_codes(recovered_codes)
        
        # Decode the data
        print("Decoding data...")
        decoded_data = codec.decode(bit_string)
        
        # Save decoded data
        output_file = base_filename + "_decompressed.txt"
        print(f"Saving decoded text to: {output_file}")
        FileHandler.write_text(output_file, decoded_data)
        
        print("\nDecompression completed successfully!")
    except Exception as e:
        print(f"An error occurred during decompression: {str(e)}")
        raise e

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py [compress|decompress] [file_path]")
        return
        
    mode = sys.argv[1]
    file_path = sys.argv[2]
    
    if mode == "compress":
        process_file(file_path)
    elif mode == "decompress":
        decompress_file(file_path)
    else:
        print("Invalid mode. Please choose 'compress' or 'decompress'.")

if __name__ == "__main__":
    main()