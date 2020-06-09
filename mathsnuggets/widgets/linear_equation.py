import sympy

from mathsnuggets.core import fields
from mathsnuggets.widgets import equation

test = {"equation": "x + 4 = 3"}


class LinearEquation(equation.Equation):
    """Linear Equations"""

    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")
    d = fields.RandomNumber("d")

    def generator(self):
        self.equation = sympy.Eq(self.a * self.x + self.b, self.c * self.x + self.d)

    @fields.constraint("One-Step")
    def one_step(self):
        return (
            self.a * self.d != 0
            and (self.a == 1 and self.b != 0 or self.b == 0 and self.d % self.a == 0)
            and self.c == 0
        )

    @fields.constraint("Two-Step")
    def two_step(self):
        return (
            self.a * self.b * self.d != 0
            and self.c == 0
            and (self.d - self.b) % self.a == 0
        )

    @fields.constraint("Multi-Step")
    def multi_step(self):
        return not self.one_step and not self.two_step
