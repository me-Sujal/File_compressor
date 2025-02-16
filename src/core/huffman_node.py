# core/huffman_node.py
class HuffmanNode:
    def __init__(self, value=None, freq=None):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
