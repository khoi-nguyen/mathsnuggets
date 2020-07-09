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
        "non-zero numbers", default=True, hidden=True, protected=True
    )
    def non_zero_numbers(self):
        self.a -= {0}
        self.b -= {0}
        self.c -= {0}
        self.d -= {0}

    @fields.constraint("same denominators")
    def same_denominators(self):
        return self.b == self.d
