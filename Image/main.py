import numpy as np
from collections import Counter
from huffman import Huffman
from priority_Q import PriorityQueue
from PIL import Image

def get_image(filename="cat.bmp"):
    with Image.open(filename) as img:
        img.load()
    return img

def create_frequency_dict(data):
    freq = dict(Counter(data.flatten()))
    converted_freq = {int(key) : value for key, value in freq.items()} 
    return converted_freq

def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def write_huff_code(data):
    filename = "huffman_code.txt"
    with open(filename, 'w') as file:
        for key, value in data.items():
            file.write(f"{key}:{value}\n")


def main():
    # Load and convert image to grayscale
    image = get_image()
    g_image = image.convert('L')
    image_arr = np.array(g_image)

    # Create frequency dictionary
    freq_dict = create_frequency_dict(image_arr)
    
    # Create priority queue from frequencies
    pq = PriorityQueue.from_frequency(freq_dict)
    
    # Create Huffman coding tree
    huffman = Huffman()
    huffman.build_huffman_tree(pq)
    codes = huffman.generate_codes()
    # print(codes)
    write_huff_code(codes)
    
    # Encode image data
    flat_data = image_arr.flatten()
    encoded_data = huffman.encode(flat_data)
    write_file("encoded.txt", encoded_data)

    # Write the encoded data
    encoded_file = "encoded.txt"
    with open(encoded_file, 'w') as file:
        file.write(encoded_data)

    # Decode the encoded data
    decoded_data = huffman.decode(encoded_data)
    decoded_array = np.array(decoded_data, dtype=np.uint8).reshape(image_arr.shape)

    # Save the decoded_image 
    decoded_image = Image.fromarray(decoded_array)
    decoded_image.save('decoded_image.jpg')    
  
if __name__ == "__main__":
    main()
