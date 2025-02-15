# core/huffman_codec.py
from collections import Counter
from .huffman_node import HuffmanNode
from .priority_queue import PriorityQueue

class HuffmanCodec:
    def __init__(self):
        self.codes = {}
        self.root = None
        self.encoded_length = 0
        
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
        freq_dict = self._calculate_frequency(data, is_image)
        self._build_tree(freq_dict)
        self._generate_codes()
        
        if is_image:
            data = data.flatten()
        
        encoded = ''.join(self.codes[value] for value in data)
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

        return ''.join(str(x) if not isinstance(x, str) else x for x in decoded)
