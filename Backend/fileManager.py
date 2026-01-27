"""Script to store and manage printing files"""

# Totally unnecessary Queue class
class Queue(list):
    def __init__(self, maxsize=0):
        super().__init__()
        self.maxsize = maxsize

    def full(self):
        return len(self) >= self.maxsize

    def empty(self):
        return len(self) == 0

    def put(self, element):
        self.append(element)

    def size(self):
        return len(self)


# Queue of files to print, at most 5
queue = Queue(5)

# Add a file to the queue
def add_to_queue(file):
    if (queue.full()):
        return False
    queue.put(file)
    return True

# Get the next file in the queue
def get_next_file_in_queue():
    if (queue.empty()):
        return None
    return queue[0]

# Return the queue
def get_queue_size():
    return queue.size()

def get_full_queue():
    return queue