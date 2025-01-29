from priority_Q import PriorityQueue


class HuffmanNode:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

class Huffman:
    def __init__(self):
        self.codes = {}
        self.root = None

    def build_huffman_tree(self, pq):
        new_queue = PriorityQueue()
        while not pq.is_empty():
            value, freq = pq.pop()
            node = HuffmanNode(value, freq)
            new_queue.push((node, freq))

        while len(new_queue.heap) > 1:
            node1, freq1 = new_queue.pop()
            node2, freq2 = new_queue.pop()

            combined = HuffmanNode(None, freq1 + freq2)
            combined.left = node1
            combined.right = node2

            new_queue.push((combined, combined.freq))
        
        if not new_queue.is_empty():
            self.root = new_queue.pop()[0]

    def generate_codes(self, node=None, code="", codes=None):
        if codes is None:
            codes = self.codes
        if node is None:
            node = self.root
            
        if node.char is not None:
            codes[node.char] = code
            return
            
        if node.left:
            self.generate_codes(node.left, code + "0", codes)
        if node.right:
            self.generate_codes(node.right, code + "1", codes)

        return codes

    def encode(self, data):
        encoded = ""
        for value in data:
            encoded += self.codes.get(int(value), '')
        return encoded

    def decode(self, encoded_data):
        decoded = []
        current = self.root
        for bit in encoded_data:
            if bit == '0':
                current = current.left
            else:
                current = current.right
            
            if current.char is not None:
                decoded.append(current.char)
                current = self.root
        return decoded


