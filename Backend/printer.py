"""Printrun logic here"""
from printrun.printcore import printcore
import asyncio

from fileManager import *

class Printer:
    def __init__(self, port: str, baud: int, connection_timeout : int = 10, max_queue_size: int = 0):
        self.connection_timeout = connection_timeout
        self.printer_queue = Queue(max_queue_size)
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

    def disconnect(self):
        self.printer.disconnect()

    def full(self):
        return self.printer_queue.full()

    def empty(self):
        return self.printer_queue.empty()

    def add_to_queue(self, element):
        return self.printer_queue.put(element)

    def queue_size(self):
        return self.printer_queue.size()

