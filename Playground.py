class Calculator(object):
    def __init__(self, arg1):
        self.arg1 = arg1
    def add(self, a, b):
        return a + b
    def subtract(self, a, b):
        return a - b
    def divide(self, a, b):
        return a / b
    def multiply(self, a, b):
        return a * b

calculator = Calculator(1)
print(calculator.multiply(3, 4))