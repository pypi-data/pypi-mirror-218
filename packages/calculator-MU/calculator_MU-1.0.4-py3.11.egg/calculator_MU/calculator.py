from math import pow


class Calculator:
    """
        A class representing a calculator.

        Attributes:
            memory (float): The current value stored in the calculator's memory.

        Methods:
            add(num): Adds the given number to the calculator's memory.
            subtract(num): Subtracts the given number from the calculator's memory.
            multiply(num): Multiplies the calculator's memory by the given number.
            divide(num): Divides the calculator's memory by the given number.
            root(num): Calculates the n-th root of the number in the calculator's memory.
            reset(): Resets the calculator's memory to 0.

        Usage:
            use the given commands(add, subtract, multiply etc.)
            to change the current memory value in the calculator.
        """

    def __init__(self):
        self.memory = 0

    def __str__(self) -> str:
        return str(self.memory)

    def add(self, num: float) -> None:
        """
        Adds the given number to the calculator's memory.

        Arguments:
            num (float): The number to be added.

        Usage:
            calculator = Calculator()
            calculator.add(5)
        """
        self.memory += num

    def subtract(self, num: float) -> None:
        """
        Subtracts the given number from the calculator's memory.

        Arguments:
            num (float): The number to be subtracted.

        Usage:
            calculator = Calculator()
            calculator.subtract(2)
        """
        self.memory -= num

    def multiply(self, num: float) -> None:
        """
        Multiplies the calculator's memory by the given number.

        Arguments:
            num (float): The number to multiply by.

        Usage:
            calculator = Calculator()
            calculator.multiply(3)
        """
        self.memory *= num

    def divide(self, num: float) -> None:
        """
        Divides the calculator's memory by the given number.

        Arguments:
            num (float): The number to divide by.

        Usage:
            calculator = Calculator()
            calculator.divide(2)
        """
        self.memory /= num

    def root(self, num: float) -> None:
        """
        Calculates the n-th root of the number in the calculator's memory.

        Arguments:
            num (float): The degree of the root.

        Usage:
            calculator = Calculator()
            calculator.memory = 16
            calculator.root(2)
        """
        self.memory = pow(self.memory, 1 / num)

    def reset(self) -> None:
        """
        Resets the calculator's memory to 0.

        Usage:
            calculator = Calculator()
            calculator.reset()
        """
        self.memory = 0
