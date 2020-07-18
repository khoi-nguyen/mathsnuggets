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
        answer = sympy.solveset(self.equation, self.x)
        if answer.func == sympy.FiniteSet and len(answer.args) <= 3:
            answer = [sympy.Eq(self.x, answer.args[i]) for i in range(len(answer.args))]
        return answer


def test_equation():
    assert isinstance(Equation(equation="x^2 - 5x + 6").solution, list)
    assert isinstance(Equation(equation="x^3 - 5x^2 + 6x").solution, list)
    assert isinstance(Equation(equation="x(x-1)(x-2)(x-3)").solution, sympy.FiniteSet)
    assert isinstance(Equation(equation="sin(x)").solution, sympy.Union)
