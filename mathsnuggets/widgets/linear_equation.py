import random

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

    @fields.constraint("Unique solution", default=True, hidden=True, protected=True)
    def unique_solution(self):
        return self.a != self.c

    @fields.range_constraint("One-Step")
    def one_step(self):
        self.c = 0
        if random.randint(0, 1):
            self.a = 1
            self.b -= {0}
        else:
            self.b = 0
            self.a -= {0}

    @fields.range_constraint("Two-Step")
    def two_step(self):
        self.c = 0
        self.a -= {0}
        self.b -= {0}
        self.d -= {0}

    @fields.range_constraint("Multi-Step")
    def multi_step(self):
        self.a -= {0}
        self.b -= {0}
        self.c -= {0}
        self.d -= {0}

    @fields.constraint("Integer solution", default=True)
    def integer_solution(self):
        return self.unique_solution and (self.d - self.b) % (self.a - self.c) == 0
