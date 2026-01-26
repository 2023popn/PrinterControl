"""Printrun logic here"""

nextFileToPrint = [""]

def loadNextFileToPrint(file):
    nextFileToPrint[0] = file

def printNextFileToPrint():
    # printrun
    if (nextFileToPrint[0]):
        return True
    return False