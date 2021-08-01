import pytest
import sympy

from mathsnuggets.core import fields, form

test = {"info": "radius", "equation": "x^2 + y^2 = 9"}


class CircleEquation(form.Form):
    """Circle radius and centre"""

    template = """
        Find the `info` of the circle whose equation is `equation`
        <div v-if="payload.info === 'radius'">
            `radius`
        </div>
        <div v-else>
            `centre`
        </div>
    """

    equation = fields.Equation("Equation", required=True)
    info = fields.Select("Info", options=["radius", "centre"])

    @fields.computed("Solution")
    def solution(self):
        (a, h, k, x, y), r = (
            sympy.symbols("a h k x y"),
            sympy.symbols("r", positive=True),
        )
        formula = a * ((x - h) ** 2 + (y - k) ** 2 - r ** 2)
        equation = sympy.expand(self.equation.args[0] - self.equation.args[1] - formula)
        system = [equation.coeff(*t) for t in [(x, 2), (y, 2), (x, 1), (y, 1), (x, 0)]]
        values = sympy.solve(system, (a, r, h, k), dict=True)
        if not values:
            raise ValueError(f"{repr(self.equation)} is not an equation for a circle")
        values = values[0]
        return {"radius": values[r], "centre": (values[h], values[k])}

    @fields.computed("Centre")
    def centre(self):
        return self.solution["centre"]

    @fields.computed("Radius")
    def radius(self):
        return self.solution["radius"]

    r = fields.RandomNumber("r")
    a = fields.RandomNumber("a")
    b = fields.RandomNumber("b")
    c = fields.RandomNumber("c")
    d = fields.RandomNumber("d")
    e = fields.RandomNumber("e")
    f = fields.RandomNumber("f")
    g = fields.RandomNumber("g")

    generator_template = """
        The generator expands the left-hand side of:
        <span class="math">
            (x - a)^2 + (y - b)^2 + cx^2 + dy^2 + ex + fy + g
            = r^2 + cx^2 + dy^2 + ex + fy + g
        </span>
    """

    def generator(self):
        x, y = sympy.symbols("x y")
        self.info = "centre"
        self.equation = sympy.Eq(
            sympy.expand(
                (x - self.a) ** 2 + (y - self.b) ** 2
                + self.c * x ** 2 + self.d * y ** 2
                + self.e * x + self.f * y
                + self.g
            ),
            self.c * x ** 2 + self.d * y ** 2
            + self.e * x + self.f * y
            + self.g + self.r ** 2
        )

    @fields.range_constraint("Only constant terms on RHS")
    def constant_rhs(self):
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0


def test_circle_equation():
    with pytest.raises(ValueError):
        CircleEquation(equation="x^2 + 1").solution

    assert CircleEquation(equation="x^2 + y^2 = 9").radius == 3
    assert CircleEquation(equation="(x-3)^2 + (y-2)^2 = 4").centre == (3, 2)
