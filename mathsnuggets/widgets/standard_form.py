import sympy

from mathsnuggets.core import fields, form


class StandardForm(form.Form):
    """Standard form"""

    template = "Calculate `index_1` `operation` `index_2` `solution`"

    index_1 = fields.StandardForm("index 1")
    index_2 = fields.StandardForm("index 2")
    operation = fields.Select("operation", options=["+", "-", "×", "÷"])

    @fields.computed("Solution", field=fields.StandardForm)
    def solution(self):
        operations = {
            "+": sympy.Add,
            "-": lambda a, b: a - b,
            "×": sympy.Mul,
            "÷": lambda a, b: a / b,
        }
        if self.operation:
            return sympy.simplify(
                operations[self.operation](self.index_1, self.index_2)
            )

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    m = fields.RandomNumber("m")
    n = fields.RandomNumber("n")
    op = fields.RandomNumber("op", default=["+", "-", "×", "÷"])

    def generator(self):
        self.index_1 = self.a * 10 ** self.m
        self.index_2 = self.b * 10 ** self.n
        self.operation = self.op

    @fields.constraint("Positive powers")
    def positive(self):
        return self.m > 0 and self.n > 0

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
