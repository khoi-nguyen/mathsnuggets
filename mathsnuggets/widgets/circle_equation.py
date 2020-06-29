import sympy

from mathsnuggets.core import fields, form

test = {"info": "radius", "equation": "x^2 + y^2 = 9"}


class CircleEquation(form.Form):
    """Circle radius and center"""

    template = "Find the `info` of the circle `equation` `solution`"

    equation = fields.Equation("Equation", required=True)
    info = fields.Select("Info", options=["radius", "center"])

    @fields.computed("Radius/Center")
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
            raise ValueError("The equation you have entered is not that of a circle")
        values = values[0]
        return values[r] if self.info == "radius" else (values[h], values[k])
