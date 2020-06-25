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
        if self.operation == "+":
            answer = self.fraction_1 + self.fraction_2
        elif self.operation == "-":
            answer = self.fraction_1 - self.fraction_2
        elif self.operation == "×":
            answer = self.fraction_1 * self.fraction_2
        else:
            answer = self.fraction_1 / self.fraction_2
        return answer

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")
    d = fields.RandomNumber("d")

    def generator(self):
        self.fraction_1 = self.a / self.b
        self.fraction_2 = self.c / self.d

    @fields.constraint("t")
    def true(self):
        return True

    @fields.range_constraint(
        "non-zero numbers", default=True, hidden=True, protected=True
    )
    def non_zero_numbers(self):
        self.a -= {0}
        self.b -= {0}
        self.c -= {0}
        self.d -= {0}
