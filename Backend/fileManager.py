"""Script to store and manage printing files"""

# Totally unnecessary Queue class
class Queue(list):
    def __init__(self, maxsize=0):
        super().__init__()
        self.maxsize = maxsize

    def full(self):
        if self.maxsize > 0:
            return len(self) >= self.maxsize
        return False

    def empty(self):
        return len(self) == 0

    def put(self, element):
        self.append(element)

    def size(self):
        return len(self)


class PrinterFile:
    def __init__(self, file):
        self.file = file
        self.print_time = self.read_print_time()
        self.target_printer = self.get_target_printer()

    def read_print_time(self) -> int | None:
        with open(self.file, 'r', encoding='utf-8') as file:
            for line in file:
                if "TIME" in line:
                    seconds = int(line.split(":")[1].strip())
                    return seconds
            return None

    def get_target_printer(self) -> str | None:
        filename = self.file.filename
        return filename.split("_")[0]



# Queue of files to print, at most 5
queue = Queue(5)

# Add a file to the queue
def add_to_queue(file):
    if queue.full():
        return False
    queue.put(file)
    return True

# Get the next file in the queue
def get_next_file_in_queue():
    if queue.empty():
        return None
    return queue[0]

# Return the queue
def get_queue_size():
    return queue.size()

def get_full_queue():
    return queue

# Functions for getting information from files
