# main.py
from core.huffman_codec import HuffmanCodec
from utils.file_handler import FileHandler
from compression import Compressor
import os

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

    # Determine if input is image
    base_filename = os.path.splitext(input_path)[0]

    try:
        # Initialize codec and compressor
        codec = HuffmanCodec()
        compressor = Compressor(base_filename + "_compressed.bin")

        # Read input
        data = FileHandler.read_text(input_path)
       
        # Encode data

        print("Encoding data...")
        encoded_data = codec.encode(data)

        # Compress data and include Huffman codes
        print("Compressing encoded data...")
        compressed_data = compressor.compress(encoded_data, codec.codes)

        # Save compressed data
        print(f"Saving compressed data to: {compressor.filename}")
        FileHandler.write_binary(compressor.filename, compressed_data)

        # Calculate compression stats
        original_size = os.path.getsize(input_path)
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
        output_file = base_filename + "_decoded.txt"
        print(f"Saving decoded text to: {output_file}")
        FileHandler.write_text(output_file, decoded_data)

        print("\nProcess completed successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e  # This will help with debugging

def decompress_file(compressed_file_path):
    if not os.path.exists(compressed_file_path):
        print(f"Error: File '{compressed_file_path}' not found!")
        return

    try:
        # Read the compressed binary file
        with open(compressed_file_path, 'rb') as f:
            compressed_data = f.read()

        # Create compressor instance
        compressor = Compressor(compressed_file_path)
        
        # Get the base filename without "_compressed.bin"
        base_filename = compressed_file_path.replace("_compressed.bin", "")

        # Decompress the data
        print("\nDecompressing data...")
        decompressed_data, recovered_codes = compressor.decompress(compressed_data)

        # Create a new HuffmanCodec instance and set its codes
        codec = HuffmanCodec()
        codec.codes = recovered_codes
        
        # Rebuild the Huffman tree from the recovered codes
        codec._build_tree({symbol: 1 for symbol in recovered_codes.keys()})

        # Determine if it's an image based on original filename
        is_image = base_filename.lower().endswith(('.bmp', '.jpg', '.png', '.jpeg'))

        # Decode the data
        print("Decoding data...")
        if is_image:
            # For images, we need the original shape
            # You might need to store this in the compressed file
            shape = None  # You'll need to modify this
            decoded_data = codec.decode(decompressed_data, shape)
            output_file = base_filename + "_decompressed.jpg"
            ImageHandler.save_image(output_file, decoded_data)
        else:
            decoded_data = codec.decode(decompressed_data)
            output_file = base_filename + "_decompressed.txt"
            FileHandler.write_text(output_file, decoded_data)

        print(f"\nDecompressed file saved as: {output_file}")

    except Exception as e:
        print(f"An error occurred during decompression: {str(e)}")
        raise e

# Modify your main() function to include decompression option:
def main():
    while True:
        print("\nHuffman Compression Tool")
        print("1. Compress text file")
        print("2. Compress image file")
        print("3. Decompress file")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '4':
            break
            
        if choice in ['1', '2']:
            input_path = input("Enter the input file path: ")
            file_extension = os.path.splitext(input_path)[1].lower()
            
            if os.path.exists(input_path):
                if choice == '1' and file_extension in ['.txt', '.log', '.md']:
                    process_file(input_path)
                elif choice == '2' and file_extension in ['.bmp', '.jpg', '.png', '.jpeg']:
                    process_file(input_path)
                else:
                    print(f"Invalid file type: {file_extension}")
            else:
                print(f"File not found: {input_path}")
        elif choice == '3':
            input_path = input("Enter the compressed file path (.bin): ")
            if os.path.exists(input_path) and input_path.endswith('.bin'):
                decompress_file(input_path)
            else:
                print("Invalid file or file not found!")
        else:
            print("Invalid choice!")

'''
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
                file_extension = os.path.splitext(input_path)[1].lower()
                
                if os.path.exists(input_path):
                    if choice == '1' and file_extension in ['.txt', '.log', '.md']:
                        process_file(input_path)
                    elif choice == '2' and file_extension in ['.bmp', '.jpg', '.png', '.jpeg']:
                        process_file(input_path)
                    else:
                        print(f"Invalid file type: {file_extension}")
                else:
                    print(f"File not found: {input_path}")
            else:
                print("Invalid choice!")'''

if __name__ == "__main__":
    main()
