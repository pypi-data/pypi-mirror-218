class Calculator:
    """
    A class representing a simple calculator.
    """

    def __init__(self):
        """
        Initializes a new instance of the Calculator class.
        """
        self.memory = 0

    def add(self, num):
        """
        Adds the specified number to the calculator's memory.

        Parameters:
            num (int or float): The number to be added.

        Returns:
            None
        """
        self.memory += num

    def subtract(self, num):
        """
        Subtracts the specified number from the calculator's memory.

        Parameters:
            num (int or float): The number to be subtracted.

        Returns:
            None
        """
        self.memory -= num

    def multiply(self, num):
        """
        Multiplies the calculator's memory by the specified number.

        Parameters:
            num (int or float): The number to multiply by.

        Returns:
            None
        """
        self.memory *= num

    def divide(self, num):
        """
        Divides the calculator's memory by the specified number.

        Parameters:
            num (int or float): The number to divide by.

        Raises:
            ValueError: If the specified number is zero.

        Returns:
            None
        """
        if num != 0:
            self.memory /= num
        else:
            raise ValueError("Cannot divide by zero.")

    def nth_root(self, num, n):
        """
        Calculates the nth root of the specified number and stores it in the calculator's memory.

        Parameters:
            num (int or float): The number to calculate the nth root of.
            n (int or float): The root index.

        Returns:
            None
        """
        self.memory = num ** (1/n)

    def reset_memory(self):
        """
        Resets the calculator's memory to zero.

        Returns:
            None
        """
        self.memory = 0
