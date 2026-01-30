"""Printrun logic here"""
from printrun.printcore import printcore
import asyncio

from fileManager import *

class Printer:
    def __init__(self, printer_queue: Queue, port: str, baud: int, connection_timeout : int = 10):
        self.connection_timeout = connection_timeout
        self.printer_queue = printer_queue
        self.port = port
        self.baud = baud

        # Initiallize printcore
        self.printer = printcore()

        # TODO Setup callbacks

    async def connect_printer_with_timeout(self):
        """
        Attempt to connect to printer with timeout.
        Raises asyncio.TimeoutError if connection takes too long.
        """
        # Start the connection
        self.printer.connect(self.port, self.baud)

        try:
            # Wait for connection with timeout (non-blocking)
            await asyncio.wait_for(
                self._wait_for_online(),
                timeout=self.connection_timeout
            )
            print("Printer connected successfully!")
            return True

        except asyncio.TimeoutError:
            # Connection timed out
            print(f"Failed to connect to printer after {self.connection_timeout} seconds")
            self.printer.disconnect()  # Clean up
            raise ConnectionError(f"Printer connection timeout after {self.connection_timeout}s")

    async def _wait_for_online(self):
        """Helper method to wait for printer to come online"""
        while not self.printer.online:
            await asyncio.sleep(0.1)



def loadNextFileToPrint(file):
    nextFileToPrint[0] = file

def printNextFileToPrint():
    # printrun
    if (nextFileToPrint[0]):
        return True
    return False