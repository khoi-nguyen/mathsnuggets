import sympy

from mathsnuggets.core import fields, form

test = {"expression": "x^2 - 5x + 6"}


class Factorise(form.Form):
    """Factorise"""

    template = "Factorise `expression` `factorisation`"

    expression = fields.Expression("expression")

    def validate(self):
        self.expression = sympy.expand(self.expression)

    @fields.computed("Factorisation")
    def factorisation(self):
        return sympy.factor(self.expression)

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")
    d = fields.RandomNumber("d")

    def generator(self):
        x = sympy.symbols("x")
        self.expression = sympy.expand((self.a * x + self.b) * (self.c * x + self.d))

    @fields.range_constraint(
        "Non-zero expression", default=True, hidden=True, protected=True
    )
    def nonzero(self):
        self.b -= {0}
        self.c -= {0}

    @fields.range_constraint("Quadratic", default=True)
    def quadratic(self):
        self.a -= {0}
        self.c -= {0}

    @fields.range_constraint("Linear")
    def linear(self):
        self.a = {0}

    @fields.range_constraint("ax^2+bx")
    def one_bracket(self):
        self.b = {0}
