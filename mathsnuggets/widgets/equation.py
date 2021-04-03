import sympy

from mathsnuggets.core import fields, form
from mathsnuggets.widgets import plot

test = {"equation": "x^2 - 5x + 6"}


class Equation(form.Form):
    """Equation"""

    equation = fields.Equation("Equation", required=True)
    x = fields.Expression("Solve for", default="x", required=True)
    template = """
        Solve `equation` for `x` `solution`
        <span v-if="config.edit">`show_graph`</span>
        <div v-if="payload.show_graph">`graph`</div>
    """
    show_graph = fields.Boolean("Show graph", default=False)
    h = fields.Expression("h", default="3")

    @fields.computed("Solution")
    def solution(self):
        answer = sympy.solveset(self.equation, self.x)
        if answer.func == sympy.FiniteSet and len(answer.args) <= 3:
            answer = [sympy.Eq(self.x, answer.args[i]) for i in range(len(answer.args))]
        return answer

    @fields.computed("Plot", field=fields.Html, nohide=True)
    def graph(self):
        args = {"functions": [self.equation.args[0], self.equation.args[1]]}
        if isinstance(self.solution, list) and len(self.solution) in [1, 2]:
            if len(self.solution) == 1:
                solution = self.solution[0].args[1]
            if len(self.solution) == 2:
                x1, x2 = self.solution[0].args[1], self.solution[1].args[1]
                solution = (x1 + x2) / 2
                self.h = x2 - solution + 2
            args.update({"x_min": solution - self.h, "x_max": solution + self.h})
        return plot.Plot(**args).plot


def test_equation():
    assert isinstance(Equation(equation="x^2 - 5x + 6").solution, list)
    assert isinstance(Equation(equation="x^3 - 5x^2 + 6x").solution, list)
    assert isinstance(Equation(equation="x(x-1)(x-2)(x-3)").solution, sympy.FiniteSet)
    assert isinstance(Equation(equation="sin(x)").solution, sympy.Union)
