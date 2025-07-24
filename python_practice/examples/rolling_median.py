from decorators import timeit_decorator
import heapq
import pandas as pd
import time
import statistics

def med(values):
    sorted_values = sorted(values.copy())
    mid = len(sorted_values) // 2
    n = len(sorted_values)

    if n % 2 == 0: # even
        return (sorted_values[mid-1] + sorted_values[mid]) / 2
    else:
        #odd
        return sorted_values[mid]

class StreamingMedian():
    def __init__(self):
        self.low = []   # stores highest first of the numbers on the lower half
        self.high = []  # stors lowest first of the numbers on the higher half

    def add(self, num):
        # push to max heap "low"
        heapq.heappush(self.low, -num)

        # balance by pushing highest from "low" to high
        heapq.heappush(self.high, -heapq.heappop(self.low))
        
        # ensure low has equal or more elements
        if len(self.low) < len(self.high):
            heapq.heappush(self.low, -heapq.heappop(self.high))
            
    def get_median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        else:
            return (-self.low[0] + self.high[0]) / 2
    
if __name__ == '__main__':
    tracker = StreamingMedian()

    #stream = [5, 15, 1, 3, 6, 9]
    stream = list(range(10000))

    start_time = time.time()
    for num in stream:
        tracker.add(num)
        tracker.get_median()
        #print(f"After inserting {num}, median = {tracker.get_median()}")
    
    print(f'\nStreamingMedian executed in: {time.time() - start_time:.04f} seconds')

    # print('\nStreamingMedian arranges stream from:')
    # print(stream)
    # print('to:')
    # print(sorted(stream))
    # print(f'\nWith the median being the central point of the ordered list ie: {tracker.get_median():.02f}')

    start_time = time.time()
    stream_history = []
    for num in stream:
        stream_history.append(num)
        #print(f'{statistics.median(stream_history)}')
        statistics.median(stream_history)
        # med(stream_history)
    print(f'\nMedian of a growing stream history executed in: {time.time() - start_time:.04f} seconds')

    start_time = time.time()
    df_stream = pd.DataFrame(stream, columns=['number'])
    df_stream['median'] = df_stream['number'].expanding(1).median()
    print(f'\nPandas rolling median executed in: {time.time() - start_time:.04f} seconds')

    # print(df_stream)


    

    pass
