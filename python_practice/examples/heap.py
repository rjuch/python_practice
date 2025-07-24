import heapq

nums = [5, 1, 8, 3]
heapq.heapify(nums)

print(nums)  # Internally rearranged as a min-heap

heapq.heappush(nums, 0)   # Insert 0
print(heapq.heappop(nums))  # → 0 (smallest)
print(heapq.heappushpop(nums, 0))   # Insert 0

class heapq_max():
    import heapq
    def __init__(self):
        pass

    def heappush(self, heap_in, num):
        heapq.heappush(heap_in, -num)

    def heappop(self, heap_in):
        return -heapq.heappop(heap_in)
    
    def heapify(self, heap_in):
        heapq.heapify([-x for x in heap_in])


# maintain k largest 
nums2 = []
heap_max = heapq_max()
# heap_max.heapify(nums2)

nums3 = [5, 2, 6, 8, 1, 4, 7, 8 , 21, 8, 2, 9, 2]
top3 = []

for num in nums3:
    heapq.heappush(top3, num)
    if len(top3) > 3:
        heapq.heappop(top3)

print(f'All numbers: {nums3}')
print(f'3 largest: {top3}')
pass

class StreamingMedian:
    def __init__(self):
        self.low = []   # max-heap (store negatives)
        self.high = []  # min-heap

    def add(self, num):
        # Step 1: Push to max-heap (low)
        heapq.heappush(self.low, -num)

        # Step 2: Balance by pushing max of low to high
        heapq.heappush(self.high, -heapq.heappop(self.low))

        # Step 3: Ensure low has equal or more elements than high
        if len(self.low) < len(self.high):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def get_median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        else:
            return (-self.low[0] + self.high[0]) / 2

tracker = StreamingMedian()

stream = [5, 15, 1, 3]
for num in stream:
    tracker.add(num)
    print(f"After inserting {num}, median = {tracker.get_median()}")

if __name__ == "__main__":
    pass