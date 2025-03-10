# core/huffman_codec.py
from collections import Counter
from .huffman_node import HuffmanNode
from .priority_queue import PriorityQueue
from .tree_viz import HuffmanTreeVisualizer

class HuffmanCodec:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}
        self.root = None
    # end of __init__

    def _build_tree(self, freq_dict):
        pq = PriorityQueue()
        for value, freq in freq_dict.items():
            node = HuffmanNode(value, freq)
            pq.push((node, freq))

        while not pq.is_empty():
            if len(pq.heap) == 1:
                self.root = pq.pop()[0]
                break

            node1, freq1 = pq.pop()
            node2, freq2 = pq.pop()

            combined = HuffmanNode(None, freq1 + freq2)
            combined.left = node1
            combined.right = node2

            pq.push((combined, combined.freq))
    # enf of build_tree

    def _generate_codes(self, node=None, code=""):
        if node is None:
            node = self.root
            self.codes = {}
            
        if node.value is not None:
            self.codes[node.value] = code
            return
            
        if node.left:
            self._generate_codes(node.left, code + "0")
        if node.right:
            self._generate_codes(node.right, code + "1")
    # end of generate_codes

    def encode(self, data):

        # removing the trailing whitespaces
        data = data.rstrip()
        # Create frequency dictionary
        freq_dict = Counter(data)

        print("Frequency dictionary:")
        for char, freq in freq_dict.items():
            if char.isspace():
                print(f"Space (ASCII {ord(char)}): {freq}")
            else:
                print(f"{char}: {freq}")
    

        self._build_tree(freq_dict)
        self._generate_codes()
        
        # Create reverse lookup for decoding
        self.reverse_codes = {code: char for char, code in self.codes.items()}
        
        # Encode the data
        encoded = ''.join(self.codes[char] for char in data)
        return encoded
    # end of encode

    def decode(self, encoded_data):
        # Use reverse lookup instead of tree traversal
        current_code = ''
        decoded = []
        
        for bit in encoded_data:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded.append(self.reverse_codes[current_code])
                current_code = ''
                
        return ''.join(decoded)
    # end of decode

    def set_codes(self, codes):
        self.codes = codes
        # Create reverse lookup for decoding
        self.reverse_codes = {code: char for char, code in codes.items()}
    # end of set_codes

    def visualize_tree(self):
        visualizer = HuffmanTreeVisualizer()
        visualizer.create_visualization(self.root)
    # end of visualize_tree
