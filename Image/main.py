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
    return dict(Counter(data.flatten()))

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
    huffman.generate_codes()
    
    # Encode image data
    flat_data = image_arr.flatten()
    encoded_data = huffman.encode(flat_data)

    # Write the encoded data
    encoded_file = "encoded.txt"
    with open(encoded_file, 'w') as file:
        file.write(encoded_data)

    # Decode the encoded data
    decoded_data = huffman.decode(encoded_data)
    decoded_array = np.array(decoded_data).reshape(image_arr.shape)

    # Save the decoded_image 
    decoded_image = Image.fromarray(decoded_array)
    decoded_image.save('decoded_image.jpg')    
  
if __name__ == "__main__":
    main()
