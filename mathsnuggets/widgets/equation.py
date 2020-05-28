import sympy

from mathsnuggets.core import fields, form


class Equation(form.Form):
    """Equation"""

    equation = fields.Equation("Equation", required=True)
    x = fields.Expression("Solve for", default="x", required=True)
    template = "Solve `equation` for `x` `solution`"

    @fields.computed("Solution")
    def solution(self):
        return sympy.solveset(self.equation, self.x)
