import sympy

from mathsnuggets.core import fields
from mathsnuggets.widgets import equation

test = {"equation": "x^2 - 3x + 2"}


class QuadraticEquations(equation.Equation):
    """Quadratic Equations"""

    a = fields.RandomNumber("a", default="-3,3")
    x1 = fields.RandomNumber("x1")
    x2 = fields.RandomNumber("x2")
    d = fields.RandomNumber("d")
    e = fields.RandomNumber("e")
    f = fields.RandomNumber("f")

    def generator(self):
        self.equation = sympy.Eq(
            sympy.expand(
                self.a * (self.x - self.x1) * (self.x - self.x2)
                + self.d * self.x ** 2
                + self.e * self.x
                + self.f
            ),
            self.d * self.x ** 2 + self.e * self.x + self.f,
        )

    @fields.range_constraint(
        "Quadratic Equation", default=True, hidden=True, protected=True
    )
    def quadratic_equation(self):
        self.a -= {0}

    @fields.constraint("No linear terms after simplification")
    def no_linear_terms(self):
        return self.x1 + self.x2 == 0

    @fields.constraint("Easy factorisation after simplification")
    def easy_factorisation(self):
        return (self.x1 + self.x2) * self.x1 * self.x2 == 0

    @fields.constraint("One (double) solution")
    def one_solution(self):
        return self.x1 == self.x2

    @fields.range_constraint("Monic after simplification")
    def monic(self):
        self.a = 1

    @fields.range_constraint("No right-hand side")
    def no_rhs(self):
        self.d = 0
        self.e = 0
        self.f = 0

    @fields.range_constraint("Constant right-hand side")
    def constant_rhs(self):
        self.d = 0
        self.e = 0
        self.f -= {0}

    @fields.range_constraint("Linear right-hand side")
    def linear_rhs(self):
        self.d = 0
        self.e -= {0}
        self.f -= {0}
