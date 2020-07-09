import random

import sympy

from mathsnuggets.core import fields, form

test = {"fraction_1": "2x/5", "fraction_2": "(4x+1)/(5x-3)", "operation": "+"}


class AlgebraicFractions(form.Form):
    """Algebraic fractions"""

    template = "Calculate `fraction_1` `operation` `fraction_2` `solution`"

    fraction_1 = fields.Expression("fraction 1")
    fraction_2 = fields.Expression("fraction 2")
    operation = fields.Select("operation", options=["+", "-", "×", "÷"])

    @fields.computed("Solution")
    def solution(self):
        operations = {
            "+": sympy.Add,
            "-": lambda a, b: a - b,
            "×": sympy.Mul,
            "÷": lambda a, b: a / b,
        }
        if self.operation:
            return sympy.simplify(
                operations[self.operation](self.fraction_1, self.fraction_2)
            )

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")
    d = fields.RandomNumber("d")
    e = fields.RandomNumber("e")
    f = fields.RandomNumber("f")
    g = fields.RandomNumber("g")
    h = fields.RandomNumber("h")
    op = fields.RandomNumber("op", default=["+", "-", "×", "÷"])

    def generator(self):
        x = sympy.symbols("x")
        self.fraction_1 = (self.a * x + self.b) / (self.c * x + self.d)
        self.fraction_2 = (self.e * x + self.f) / (self.g * x + self.h)
        self.operation = self.op

    @fields.range_constraint("One fraction normal")
    def normal(self):
        if random.randint(0, 1):
            self.a = 0
            self.c = 0
        else:
            self.e = 0
            self.g = 0

    @fields.constraint("Add")
    def add(self):
        return self.op == "+"

    @fields.constraint("Subtract")
    def subtract(self):
        return self.op == "-"

    @fields.constraint("Multiply")
    def multiply(self):
        return self.op == "×"

    @fields.constraint("Divide")
    def divide(self):
        return self.op == "÷"
