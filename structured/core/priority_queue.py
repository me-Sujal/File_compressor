# core/priority_queue.py
class PriorityQueue:
    def __init__(self):
        self.heap = []
        
    def parent(self, i):
        return (i - 1) // 2
        
    def left_child(self, i):
        return 2 * i + 1
        
    def right_child(self, i):
        return 2 * i + 2
        
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)
        
    def pop(self):
        if not self.heap:
            return None
            
        if len(self.heap) == 1:
            return self.heap.pop()
            
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        
        return root
        
    def _sift_up(self, i):
        while i > 0 and self.heap[self.parent(i)][1] > self.heap[i][1]:
            self.swap(i, self.parent(i))
            i = self.parent(i)
            
    def _sift_down(self, i):
        min_index = i
        size = len(self.heap)
        
        while True:
            left = self.left_child(i)
            right = self.right_child(i)
            
            if left < size and self.heap[left][1] < self.heap[min_index][1]:
                min_index = left
                
            if right < size and self.heap[right][1] < self.heap[min_index][1]:
                min_index = right
                
            if min_index == i:
                break
                
            self.swap(i, min_index)
            i = min_index

    def is_empty(self):
        return len(self.heap) == 0
