import sympy

from mathsnuggets.core import fields, form

test = {"fraction": "2/6"}


class SimplifyFractions(form.Form):
    """Simplify fractions"""

    template = "Simplify `fraction` `simplification`"

    fraction = fields.Expression("fraction")

    @fields.computed("Simplification")
    def simplification(self):
        return sympy.simplify(self.fraction)

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")
    d = fields.RandomNumber("d")

    def generator(self):
        x = sympy.symbols("x")
        self.fraction = (self.a * x + self.b) / (self.c * x + self.d)

    @fields.range_constraint("Numeric fraction")
    def numeric_fraction(self):
        self.a = 0
        self.c = 0
