"""Printrun logic here"""
from printrun.printcore import printcore

from fileManager import *

class Printer(printcore):
    """Printer functionality built on top of printcore

    Parameters
    ----------
    printer_queue : Queue
        Queue object that stores files. Each printer has its own queue.
    port : str, optional
        From printcore
    baud : int, optional
        From printcore
    dtr : bool, optional
        From printcore

    """
    def __init__(self, printer_queue: Queue, port: str, baud: int, dtr: bool):
        super().__init__(self)
        self.printer_queue = printer_queue

def loadNextFileToPrint(file):
    nextFileToPrint[0] = file

def printNextFileToPrint():
    # printrun
    if (nextFileToPrint[0]):
        return True
    return False