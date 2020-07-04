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

    @property
    def b(self):
        return -self.a * (self.x1 + self.x2)

    @property
    def c(self):
        return self.a * self.x1 * self.x2

    @property
    def delta(self):
        """Discriminant"""
        return self.b ** 2 - 4 * self.a * self.c

    @property
    def alpha(self):
        """x-coordinate of the turning point"""
        return -self.b / (2 * self.a)

    @property
    def beta(self):
        """y-coordinate of the turning point"""
        return -self.delta / (4 * self.a)

    @fields.range_constraint(
        "Quadratic Equation", default=True, hidden=True, protected=True
    )
    def quadratic_equation(self):
        self.a -= {0}

    @fields.constraint("No linear terms after simplification")
    def no_linear_terms(self):
        return self.b == 0

    @fields.constraint("Easy factorisation after simplification")
    def easy_factorisation(self):
        return self.b * self.c == 0

    @fields.constraint("Turning point has integer coordinates")
    def integer_turning_point(self):
        return self.alpha.is_integer and self.beta.is_integer

    @fields.constraint("Repeated roots")
    def one_solution(self):
        return self.delta == 0

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
