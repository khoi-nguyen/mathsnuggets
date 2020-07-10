import random

import sympy

from mathsnuggets.core import fields, form

test = {"fraction_1": "1/3", "fraction_2": "1/2", "operation": "+"}


class FractionOperations(form.Form):
    """Fractions"""

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
            return sympy.nsimplify(
                operations[self.operation](self.fraction_1, self.fraction_2)
            )

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")
    d = fields.RandomNumber("d")
    op = fields.RandomNumber("op", default=["+", "-", "×", "÷"])

    def generator(self):
        self.fraction_1 = self.a / self.b
        self.fraction_2 = self.c / self.d
        self.operation = self.op

    @fields.range_constraint(
        "Non-zero numbers", default=True, hidden=True, protected=True
    )
    def non_zero_numbers(self):
        self.a -= {0}
        self.b -= {0}
        self.c -= {0}
        self.d -= {0}

    @fields.range_constraint("One numerator is 1")
    def numerator_1(self):
        if random.randint(0, 1):
            self.a = 1
        else:
            self.c = 1

    @fields.constraint("First fraction is proper")
    def fraction_1_proper(self):
        return self.a < self.b

    @fields.constraint("Second fraction is proper")
    def fraction_2_proper(self):
        return self.c < self.d

    @fields.constraint("First fraction is improper")
    def fraction_1_improper(self):
        return self.a > self.b

    @fields.constraint("Second fraction is improper")
    def fraction_2_improper(self):
        return self.c > self.d

    @fields.constraint("Same denominators")
    def same_denominators(self):
        return self.b == self.d

    @fields.constraint("Addition")
    def addition(self):
        return self.op == "+"

    @fields.constraint("Subtraction")
    def subtraction(self):
        return self.op == "-"

    @fields.constraint("Multiplication")
    def multiplication(self):
        return self.op == "×"

    @fields.constraint("Division")
    def division(self):
        return self.op == "÷"
