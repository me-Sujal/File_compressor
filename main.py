# main.py
from huffman import HuffmanTree

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_encoded_file(file_path, encoded_text):
    with open(file_path, 'w') as file:
        file.write(encoded_text)

def main():
    input_file = 'text.txt'  # Path to input text file
    output_file = 'encoded.txt'  # Path to save encoded output file
    
    text = read_file(input_file)
    huffman_tree = HuffmanTree(text)
    
    encoded_text = huffman_tree.get_encoded_text()
    write_encoded_file(output_file, encoded_text)
    
    print("Huffman Codes for each character:")
    for char, code in huffman_tree.get_codes().items():
        print(f"Character: {char}, Code: {code}")

if __name__ == "__main__":
    main()
