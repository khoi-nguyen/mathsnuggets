import sympy

from mathsnuggets.core import fields
from mathsnuggets.widgets import equation

test = {"equation": "x^2 - 3x + 2"}


class QuadraticEquations(equation.Equation):
    """Quadratic Equations"""

    a = fields.RandomNumber("a")
    x1 = fields.RandomNumber("x1")
    x2 = fields.RandomNumber("x2")

    def generator(self):
        self.equation = sympy.expand(
            sympy.Eq(self.a * (self.x - self.x1) * (self.x - self.x2))
        )

    @fields.range_constraint(
        "Non-zero expression", default=True, hidden=True, protected=True
    )
    def nonzero_expression(self):
        self.a -= {0}
