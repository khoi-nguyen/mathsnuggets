import sympy

from mathsnuggets.core import fields, form

test = {"equation": "x^2 - 5x + 6"}


class Equation(form.Form):
    """Equation"""

    equation = fields.Equation("Equation", required=True)
    x = fields.Expression("Solve for", default="x", required=True)
    template = "Solve `equation` for `x` `solution`"

    @fields.computed("Solution")
    def solution(self):
        return sympy.solveset(self.equation, self.x)
