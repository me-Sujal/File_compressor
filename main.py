from huffman import HuffmanTree

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    input_file = 'text.txt'      
    encoded_file = 'encoded.txt' 
    decoded_file = 'decoded.txt' 
    
    text = read_file(input_file)
    
    huffman_tree = HuffmanTree(text)
    encoded_text = huffman_tree.get_encoded_text()
    
    write_file(encoded_file, encoded_text)
    
    print("Huffman Codes for each character:")
    for char, code in huffman_tree.get_codes().items():
        print(f"Character: {char}, Code: {code}")
    
    decoded_text = huffman_tree.decode(encoded_text)

    write_file(decoded_file, decoded_text)

    print(f"Decoded text has been saved to '{decoded_file}'.")

if __name__ == "__main__":
    main()
