"""Script to store and manage printing files"""

# Imports
from queue import Queue

# Queue of files to print, at most 5
q = Queue(maxsize=5)

# Add a file to the queue
def addToQueue(file):
    if (q.full()):
        return False
    q.put(file)
    return True

# Get the next file in the queue
def getNextFileInQueue():
    if (q.empty()):
        return None
    return q.get()

# Return the queue
def getQueueSize():
    return q.qsize()