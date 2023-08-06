# Calculator Package

The Calculator package is a Python package that provides a Calculator class for performing basic mathematical operations. This package allows you to perform addition, subtraction, multiplication, division, take the nth root of a number, and reset the calculator's memory.

## Table of Contents
- [Files](#files)
- [Installation](#installation)
- [Usage](#usage)
  - [Creating an Instance of the Calculator](#creating-an-instance-of-the-calculator)
  - [Performing Basic Operations](#performing-basic-operations)
  - [Taking the nth Root](#taking-the-nth-root)
  - [Resetting the Calculator's Memory](#resetting-the-calculators-memory)
  - [Accessing the Calculator's Memory](#accessing-the-calculators-memory)
- [Examples](#examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Files

The calculator package consists of the following files:

- `__init__.py`: This file is an empty file that is required to mark the "calculator" directory as a Python package. It allows you to organize your code and modules into a package structure.

- `calculator.py`: This file contains the implementation of the Calculator class. The Calculator class provides methods to perform mathematical operations and manage the calculator's memory. Here's an overview of the methods available in the Calculator class:

  - `__init__(self)`: Initializes the Calculator object with its memory set to 0.
  
  - `add(self, num)`: Adds a number to the calculator's memory.
  
  - `subtract(self, num)`: Subtracts a number from the calculator's memory.
  
  - `multiply(self, num)`: Multiplies the calculator's memory by a number.
  
  - `divide(self, num)`: Divides the calculator's memory by a number.
  
  - `nth_root(self, num, n)`: Takes the nth root of a number and sets it as the calculator's memory.
  
  - `reset_memory(self)`: Resets the calculator's memory to 0.

- `test_calculator.py`: This file contains unit tests for the Calculator class. It uses the `unittest` module to define test cases for each method in the Calculator class. The tests ensure that the methods of the Calculator class are functioning correctly. Running the test_calculator.py file executes the tests and verifies the expected behavior of the Calculator class.

## Installation

To install the Calculator package, you can use `pip`, the package installer for Python. Open a terminal or command prompt and run the following command:

```bash
!pip install path/to/calculator-package-1.0.0.tar.gz
```
Replace path/to/calculator-package-1.0.0.tar.gz with the actual path to the distribution file.

## Usage

To use the Calculator class, you need to import it in your Python script:

```python
from calculator import Calculator
```

### Creating an Instance of the Calculator

To start using the calculator, create an instance of the Calculator class:

```python
calculator = Calculator()
```

### Performing Basic Operations

You can perform basic mathematical operations on the calculator's memory using the following methods:

- `add(num)`: Adds a number to the calculator's memory.
  
- `subtract(num)`: Subtracts a number from the calculator's memory.
  
- `multiply(num)`: Multiplies the calculator's memory by a number.
  
- `divide(num)`: Divides the calculator's memory by a number.

Here's an example of using these methods:

```python
calculator.add(5)
calculator.subtract(3)
calculator.multiply(2)
calculator.divide(4)
```

### Taking the nth Root

You can take the nth root of a number using the `nth_root` method. Provide the number and the value of n as arguments:

```python
calculator.nth_root(16, 2)  # Taking the square root of 16
```

### Resetting the Calculator's Memory

You can reset the calculator's memory to 0 using the `reset_memory` method:

```python
calculator.reset_memory()
```

### Accessing the Calculator's Memory

You can access the value stored in the calculator's memory using the `memory` attribute:

```python
print(calculator.memory)
```

## Examples

Here are a few examples to showcase the functionality of the Calculator package:

```python
from calculator import Calculator

# Create an instance of the Calculator
calculator = Calculator()

# Perform calculations
calculator.add(5)
calculator.subtract(2)
calculator.multiply(3)
calculator.divide(4)
calculator.nth_root(16, 2)
print(calculator.memory)  # Output: 2.0

# Reset the memory
calculator.reset_memory()
print(calculator.memory)  # Output: 0
```

## Testing

The Calculator package includes unit tests to verify the correctness of the Calculator class. The test_calculator.py file contains the test cases for each method in the Calculator class. To run the tests, execute the following command:

```bash
python -m unittest test_calculator.py
```

The tests will run, and you will see the test results displayed in the terminal. Each test case checks the expected behavior of a specific method in the Calculator class. If all the tests pass, it means that the Calculator class is functioning correctly.

## Contributing

If you find any issues or have suggestions for improvement, please feel free to contribute by submitting a pull request or creating an issue on the [GitHub repository](https://github.com/TuringCollegeSubmissions/lsitsh-DWWP.1/calculator-package).

You can contribute by following these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Implement your changes and ensure that they follow the PEP8 coding standards.
4. Write tests to cover the new functionality or verify the bug fix.
5. Commit your changes and push them to your forked repository.
6. Submit a pull request to the main repository, explaining the purpose and details of your contribution.
7. We appreciate your contributions and will review them as soon as possible.

## License

This package is not licensed. It is a learning project and can be used for educational purposes only.
