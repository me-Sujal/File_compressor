# main.py
from core.huffman_codec import HuffmanCodec
from utils.file_handler import FileHandler
from utils.image_handler import ImageHandler
from compression import Compressor
import os
import sys

def write_huffman_codes(codes, filename="huffman_codes.txt"):
    with open(filename, 'w') as f:
        for char, code in sorted(codes.items()):
            if isinstance(char, str) and (char.isspace() or len(char) == 1):
                f.write(f"ASCII {ord(char)}: {char!r} -> {code}\n")
            else:
                f.write(f"Value {char} -> {code}\n")

def process_file(input_path):
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found!")
        return

    # Determine if input is image
    is_image = input_path.lower().endswith(('.bmp', '.jpg', '.png', '.jpeg'))
    base_filename = os.path.splitext(input_path)[0]

    try:
        # Initialize codec and compressor
        codec = HuffmanCodec()
        compressor = Compressor(base_filename + "_compressed.bin")

        # Read input
        print(f"\nReading input file: {input_path}")
        if is_image:
            data = ImageHandler.read_image(input_path)
            original_shape = data.shape
        else:
            data = FileHandler.read_text(input_path)
            original_shape = None

        # Encode data
        print("Encoding data...")
        encoded_data = codec.encode(data, is_image=is_image)

        # Save Huffman codes
        codes_file = base_filename + "_huffman_codes.txt"
        print(f"Saving Huffman codes to: {codes_file}")
        write_huffman_codes(codec.codes, codes_file)

        # Compress data
        print("Compressing encoded data...")
        compressed_data = compressor.compress(encoded_data)

        # Save compressed data
        print(f"Saving compressed data to: {compressor.filename}")
        FileHandler.write_binary(compressor.filename, compressed_data)

        # Calculate compression stats
        original_size = len(data.tobytes()) if is_image else len(data.encode('utf-8'))
        compressed_size = len(compressed_data)
        compression_ratio = (1 - compressed_size / original_size) * 100

        print("\nCompression Statistics:")
        print(f"Original size: {original_size} bytes")
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Compression ratio: {compression_ratio:.2f}%")

        # Decompress and verify
        print("\nTesting decompression...")
        decompressed_data = compressor.decompress(compressed_data)
        decoded_data = codec.decode(decompressed_data, original_shape)

        # Save decoded data
        if is_image:
            output_file = base_filename + "_decoded.png"
            print(f"Saving decoded image to: {output_file}")
            ImageHandler.save_image(output_file, decoded_data)
        else:
            output_file = base_filename + "_decoded.txt"
            print(f"Saving decoded text to: {output_file}")
            FileHandler.write_text(output_file, decoded_data)

        print("\nProcess completed successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    if len(sys.argv) > 1:
        # If file provided as command line argument
        input_path = sys.argv[1]
        process_file(input_path)
    else:
        # Interactive mode
        while True:
            print("\nHuffman Compression Tool")
            print("1. Compress text file")
            print("2. Compress image file")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == '3':
                break
                
            if choice in ['1', '2']:
                input_path = input("Enter the input file path: ")
                if os.path.exists(input_path):
                    if choice == '1' and input_path.endswith(('.txt', '.log', '.md')):
                        process_file(input_path)
                    elif choice == '2' and input_path.lower().endswith(('.bmp', '.jpg', '.png', '.jpeg')):
                        process_file(input_path)
                    else:
                        print("Invalid file type for selected option!")
                else:
                    print(f"File not found: {input_path}")
            else:
                print("Invalid choice!")

if __name__ == "__main__":
    main()
