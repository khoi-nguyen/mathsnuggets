import sympy

from mathsnuggets.core import fields
from mathsnuggets.widgets import equation

test = {"equation": "x^2 - 3x + 2"}


class QuadraticEquations(equation.Equation):
    """Quadratic Equations"""

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")

    def generator(self):
        self.equation = sympy.Eq(self.a * self.x ** 2 + self.b * self.x + self.c)

    @fields.range_constraint("Quadratic", default=True, hidden=True, protected=True)
    def quadratic(self):
        self.a -= {0}
