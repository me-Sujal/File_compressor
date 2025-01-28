class MinHeapNode:
    def __init__(self, data, freq):
        self.data = data
        self.freq = freq
        self.left = None  # Initialize left child
        self.right = None  # Initialize right child

class MinHeap:
    def __init__(self):
        self.heap = []

    def __heapify(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < len(self.heap) and self.heap[left].freq < self.heap[smallest].freq:
            smallest = left
        if right < len(self.heap) and self.heap[right].freq < self.heap[smallest].freq:
            smallest = right
        if smallest != index:
            self.heap[smallest], self.heap[index] = self.heap[index], self.heap[smallest]
            self.__heapify(smallest)

    def insert(self, node):
        self.heap.append(node)
        index = len(self.heap) - 1
        while index > 0 and self.heap[(index - 1) // 2].freq > self.heap[index].freq:
            self.heap[index], self.heap[(index - 1) // 2] = self.heap[(index - 1) // 2], self.heap[index]
            index = (index - 1) // 2

    def extract_min(self):
        if len(self.heap) == 0:
            return None
        root = self.heap[0]
        last_node = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = last_node
            self.__heapify(0)
        return root

    def size(self):
        return len(self.heap)

    def build_heap(self):
        for i in range((len(self.heap) // 2) - 1, -1, -1):
            self.__heapify(i)

    def is_empty(self):
        return len(self.heap) == 0
