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


def test_circle_equation():
    with pytest.raises(ValueError):
        CircleEquation(equation="x^2 + 1").solution

    assert CircleEquation(equation="x^2 + y^2 = 9").radius == 3
    assert CircleEquation(equation="(x-3)^2 + (y-2)^2 = 4").centre == (3, 2)
