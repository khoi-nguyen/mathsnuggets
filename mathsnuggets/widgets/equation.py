import sympy

from mathsnuggets.core import fields, form
from mathsnuggets.widgets import plot

test = {"equation": "x^2 - 5x + 6"}


class Equation(form.MarkedForm):
    """Equation"""

    answer = fields.ExpressionList("Your answer", nosave=True, editable=True)
    equation = fields.Equation("Equation", required=True)
    x = fields.Expression("Solve for", default="x", required=True)
    template = """
        Solve `equation` <span v-if="config.edit || payload.x !== 'x'">for `x`</span>
        <div v-if="!payload.marked_question">`solution`</div>
        <div v-else>
            <survey
                :correct="computed.correct"
                :value="payload.answer">
                Solution(s): `x` = `answer`
            </survey>
        </div>
        <div v-if="payload.show_graph">`graph`</div>
    """
    show_graph = fields.Boolean("Show graph", default=False, setting=True)
    marked_question = fields.Boolean("Marked question", default=False, setting=True)
    h = fields.Expression("h", default="3")

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if not self.answer:
            return False
        solution = sympy.solveset(self.equation, self.x)
        sol_count = len(solution.args)
        # Prevent user from just copying the equation
        for sol in self.answer:
            if len(sol.atoms(sympy.Symbol)) or sol not in solution:
                return False
        return len(solution.intersect(sympy.FiniteSet(*self.answer)).args) >= sol_count

    @fields.computed("Solution")
    def solution(self):
        answer = sympy.solveset(self.equation, self.x)
        if answer.func == sympy.FiniteSet and len(answer.args) <= 3:
            answer = [sympy.Eq(self.x, answer.args[i]) for i in range(len(answer.args))]
        return answer

    @fields.computed("Plot", field=fields.Html, nohide=True)
    def graph(self):
        if not self.show_graph:
            return ""
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

    def validate(self):
        if self.marked_question:
            if self.show_graph:
                self.show_graph = False
            if not self.name:
                super().validate()


def test_equation():
    assert isinstance(Equation(equation="x^2 - 5x + 6").solution, list)
    assert isinstance(Equation(equation="x^3 - 5x^2 + 6x").solution, list)
    assert isinstance(Equation(equation="x(x-1)(x-2)(x-3)").solution, sympy.FiniteSet)
    assert isinstance(Equation(equation="sin(x)").solution, sympy.Union)
    assert Equation(equation="x(x-1)(x-2)(x-3)", answer="0,1,2,3").correct
    assert not Equation(equation="x^2-5x+6", answer="2,3,0").correct
