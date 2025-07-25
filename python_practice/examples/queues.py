import queue

# Create a FIFO queue with optional max size
q = queue.Queue(maxsize=5)
# queue.LifoQueue
# queue.PriorityQueue

# Put items into the queue
q.put("task1")
q.put("task2")
q.put("task3")
q.put("task4")
q.put("task5")

# Get items from the queue
print(q.get())  # → "task1"
print(q.get())  # → "task2"

# Check if queue is empty
print(q.empty())  # → True