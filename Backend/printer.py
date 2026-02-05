"""Printrun logic here"""
from printrun.printcore import printcore
from printrun import gcoder
import time
import asyncio

from fileManager import *

class Printer:
    def __init__(self, port: str, baud: int, connection_timeout : int = 10, name : str = None, max_queue_size: int = 0):
        self.printer = printcore()
        self.printer.onlinecb = self.handle_printer_online
        self.printer.recvcb = self.handle_printer_response
        self.printer.endcb = self.handle_print_complete

        self.port = port
        self.baud = baud
        self.connection_timeout = connection_timeout
        self.name = name or f"Printer-{port}"
        self.queue = Queue(max_queue_size)
        self.is_connected = False
        self.is_printing = False
        self.printer_id = None  # Will be set when added to list

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

    async def add_to_queue(self, file: PrinterFile):
        """Add file to queue"""
        self.queue.put(file)

        if not self.is_connected and not self.printer.online:
            try:
                await self.connect_printer_with_timeout()
            except ConnectionError as e:
                self.queue.remove(file)
                raise

    def get_status(self):
        """Get printer status as dict"""
        return {
            "id": self.printer_id,
            "name": self.name,
            "port": self.port,
            "queue_length": len(self.queue),
            "is_connected": self.is_connected,
            "is_printing": self.is_printing,
            "printer_online": self.printer.online
        }

    # ========== Callbacks ===========

    def handle_printer_online(self):
        """Callback when printer connects"""
        print(f"{self.name} is online!")
        self.is_connected = True

    def handle_printer_response(self, line):
        """Handle printer responses"""
        print(f"{self.name}: {line}")

    def handle_print_complete(self):
        """Callback when print ends"""
        self.is_printing = False
        print(f"{self.name} print complete!")

    # ========== JSON Dictionary ===========
    def to_dict(self):
        """Convert printer object to JSON-compatible dictionary"""
        return {
            "id": self.printer_id,
            "name": self.name,
            "port": self.port,
            "baud": self.baud,
            "is_connected": self.is_connected,
            "is_printing": self.is_printing,
            "printer_online": self.printer.online,
            "connection_timeout": self.connection_timeout,
            # Add any other fields you want to send
        }