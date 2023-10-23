"""Python serial number generator."""

class SerialGenerator:
    def __init__(self, start=0):
        """Initialize serial generator with start number"""
        self.start = self.next = start

    def generate(self):
        """Return the next serial number"""
        number = self.next
        self.next += 1
        return number

    def reset(self):
        """Reset the generator to the original start number"""
        self.next = self.start

        """Initialize serial generator with start number"""

    """Machine to create unique incrementing serial numbers.
    
    >>> serial = SerialGenerator(start=100)

    >>> serial.generate()
    100

    >>> serial.generate()
    101

    >>> serial.generate()
    102

    >>> serial.reset()

    >>> serial.generate()
    100
    """

