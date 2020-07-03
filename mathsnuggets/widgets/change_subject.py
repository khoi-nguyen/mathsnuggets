import sympy

from mathsnuggets.core import fields, form

test = {"equation": "y=mx+c"}


class ChangeSubject(form.Form):
    """Change the subject"""

    template = "Make `variable` the subject for `equation` `solution`"

    equation = fields.Equation("Equation", required=True)
    variable = fields.Expression("Solve for", default="x", required=True)

    @fields.computed("Solution")
    def solution(self):
        solution = sympy.solve(self.equation, self.variable)
        if not solution:
            raise ValueError(repr(self.equation) + " cannot be solved")
        return sympy.Eq(self.variable, solution[0])
