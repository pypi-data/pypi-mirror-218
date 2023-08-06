import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.calculator.add(2)
        self.assertEqual(self.calculator.memory, 2)

    def test_subtract(self):
        self.calculator.subtract(1)
        self.assertEqual(self.calculator.memory, -1)

    def test_multiply(self):
        self.calculator.memory = 3
        self.calculator.multiply(4)
        self.assertEqual(self.calculator.memory, 12)

    def test_divide(self):
        self.calculator.memory = 10
        self.calculator.divide(2)
        self.assertEqual(self.calculator.memory, 5)

    def test_root(self):
        self.calculator.memory = 16
        self.calculator.root(2)
        self.assertEqual(self.calculator.memory, 4)

    def test_reset(self):
        self.calculator.memory = 10
        self.calculator.reset()
        self.assertEqual(self.calculator.memory, 0)


if __name__ == '__main__':
    unittest.main()



