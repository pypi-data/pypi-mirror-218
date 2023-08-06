import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """
    A test suite for the Calculator class.
    """

    def test_add(self):
        """
        Test case for the 'add' method of the Calculator class.
        """
        calculator = Calculator()  # Create an instance of the Calculator class
        calculator.add(2)  # Call the 'add' method with argument 2
        self.assertEqual(calculator.memory, 2)  # Assert that the value in calculator.memory is equal to 2

    def test_subtract(self):
        """
        Test case for the 'subtract' method of the Calculator class.
        """
        calculator = Calculator()  # Create an instance of the Calculator class
        calculator.subtract(3)  # Call the 'subtract' method with argument 3
        self.assertEqual(calculator.memory, -3)  # Assert that the value in calculator.memory is equal to -3

    def test_multiply(self):
        """
        Test case for the 'multiply' method of the Calculator class.
        """
        calculator = Calculator()  # Create an instance of the Calculator class
        calculator.memory = 4  # Set the value of calculator.memory to 4
        calculator.multiply(2)  # Call the 'multiply' method with argument 2
        self.assertEqual(calculator.memory, 8)  # Assert that the value in calculator.memory is equal to 8

    def test_divide(self):
        """
        Test case for the 'divide' method of the Calculator class.
        """
        calculator = Calculator()  # Create an instance of the Calculator class
        calculator.memory = 10  # Set the value of calculator.memory to 10
        calculator.divide(2)  # Call the 'divide' method with argument 2
        self.assertEqual(calculator.memory, 5)  # Assert that the value in calculator.memory is equal to 5

    def test_nth_root(self):
        """
        Test case for the 'nth_root' method of the Calculator class.
        """
        calculator = Calculator()  # Create an instance of the Calculator class
        calculator.nth_root(16, 2)  # Call the 'nth_root' method with arguments 16 and 2
        self.assertEqual(calculator.memory, 4)  # Assert that the value in calculator.memory is equal to 4

    def test_reset_memory(self):
        """
        Test case for the 'reset_memory' method of the Calculator class.
        """
        calculator = Calculator()  # Create an instance of the Calculator class
        calculator.memory = 7  # Set the value of calculator.memory to 7
        calculator.reset_memory()  # Call the 'reset_memory' method
        self.assertEqual(calculator.memory, 0)  # Assert that the value in calculator.memory is equal to 0


if __name__ == '__main__':
    unittest.main()
