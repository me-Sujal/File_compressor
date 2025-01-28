# huffman.py
from minheap import MinHeap, MinHeapNode

class HuffmanTree:
    def __init__(self, text):
        self.text = text
        self.frequency = self.calculate_frequency()
        self.heap = self.build_min_heap()
        self.codes = {}
        self.root = self.build_tree()
        self.generate_codes()

    def calculate_frequency(self):
        freq = {}
        for char in self.text:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
        return freq

    def build_min_heap(self):
        heap = MinHeap()
        for char, freq in self.frequency.items():
            node = MinHeapNode(char, freq)
            heap.insert(node)
        return heap

    def build_tree(self):
        while self.heap.size() > 1:
            left = self.heap.extract_min()
            right = self.heap.extract_min()
            merged_node = MinHeapNode(None, left.freq + right.freq)
            merged_node.left = left  # Set left child
            merged_node.right = right  # Set right child
            self.heap.insert(merged_node)
        return self.heap.extract_min()

    def generate_codes(self, node=None, current_code=""):
        if node is None:
            node = self.root
        if node is not None:
            if node.data:
                self.codes[node.data] = current_code
            if node.left:
                self.generate_codes(node.left, current_code + "0")
            if node.right:
                self.generate_codes(node.right, current_code + "1")

    def get_encoded_text(self):
        return ''.join(self.codes[char] for char in self.text)

    def get_codes(self):
        return self.codes
