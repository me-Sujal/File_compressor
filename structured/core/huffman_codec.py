# huffman/huffman_codec.py
from collections import Counter
import numpy as np
from .huffman_node import HuffmanNode
from .priority_queue import PriorityQueue

class HuffmanCodec:
    def __init__(self):
        self.codes = {}
        self.root = None
        self.encoded_length = 0
        
    def _calculate_frequency(self, data, is_image):
        if is_image:
            data = data.flatten()
        return dict(Counter(data))

    def _build_tree(self, freq_dict):
        # Create priority queue from frequencies
        pq = PriorityQueue()
        for value, freq in freq_dict.items():
            node = HuffmanNode(value, freq)
            pq.push((node, freq))

        # Build the tree
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

    def encode(self, data, is_image=False):
        # Calculate frequencies and build tree
        freq_dict = self._calculate_frequency(data, is_image)
        self._build_tree(freq_dict)
        self._generate_codes()
        
        # Encode the data
        if is_image:
            data = data.flatten()
        
        encoded = ""
        for value in data:
            encoded += self.codes[value]
            
        self.encoded_length = len(encoded)
        return encoded

    def decode(self, encoded_data, original_shape=None):
        decoded = []
        current = self.root
        
        for bit in encoded_data:
            if bit == '0':
                current = current.left
            else:
                current = current.right
                
            if current.value is not None:
                decoded.append(current.value)
                current = self.root

        if original_shape:
            return np.array(decoded, dtype=np.uint8).reshape(original_shape)
        return ''.join(map(str, decoded))
