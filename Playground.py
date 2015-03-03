class Calculator(object):
    def add(self, a, b):
        return a + b
    def subtract(self, a, b):
        return a - b
    def divide(self, a, b):
        return a / b
    def multiply(self, a, b):
        return a * b

calculator = Calculator()
while True:
    operation = str(input("Do you want to add (A), subtract (S), divide (D), multiply (M) or quit (Q)?  ")).lower()
    if operation != "q":
        operator1 = int(input("Enter first number: "))
        operator2 = int(input("Enter second number: "))
    if operation == "a":
        print(calculator.add(operator1, operator2))
    elif operation == "s":
        print(calculator.subtract(operator1, operator2))
    elif operation == "d":
        print(calculator.divide(operator1, operator2))
    elif operation == "m":
        print(calculator.subtract(operator1, operator2))
    elif operation == "q":
        quit()
    else:
        print("Not a valid input")


