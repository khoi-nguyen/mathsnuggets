import sympy

from mathsnuggets.core import fields, form

test = {
    "equation_1": "x + 2 = y",
    "equation_2": " 2x = y",
    "x": "x",
    "y": "y",
}


class SimultaneousEquations(form.Form):
    """Simultaneous equations"""

    template = "Solve `equation_1` and `equation_2` for `x` and `y` `solution`"

    equation_1 = fields.Equation("equation 1", required=True)
    equation_2 = fields.Equation("equation 2", required=True)
    x = fields.Expression("variable 1", default="x", required=True)
    y = fields.Expression("variable 2", default="y", required=True)

    @fields.computed("Solution")
    def solution(self):
        answer = sympy.solve([self.equation_1, self.equation_2], self.x, self.y)
        return [sympy.Eq(key, value) for key, value in answer.items()]
