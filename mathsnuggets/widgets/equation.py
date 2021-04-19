import uuid
import sympy

from mathsnuggets.core import fields, form
from mathsnuggets.widgets import plot

test = {"equation": "x^2 - 5x + 6"}


class Equation(form.Form):
    """Equation"""

    name = fields.Field("Survey name")
    answer = fields.ExpressionList("Your answer", nosave=True, editable=True)
    equation = fields.Equation("Equation", required=True)
    x = fields.Expression("Solve for", default="x", required=True)
    template = """
        Solve `equation` <span v-if="config.edit || payload.x !== 'x'">for `x`</span>
        <div v-if="!payload.marked_question">`solution`</div>
        <div v-else>
            <survey
                :name="payload.name"
                :showStats="config.authState.loggedIn"
                :correct="computed.correct"
                :value="payload.answer">
                Solution(s): `x` = `answer`
            </survey>
        </div>
        <div v-if="config.edit">
            `show_graph`
            `marked_question`
        </div>
        <div v-if="payload.show_graph">`graph`</div>
    """
    show_graph = fields.Boolean("Show graph", default=False)
    marked_question = fields.Boolean("Marked question", default=False)
    h = fields.Expression("h", default="3")

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if not self.answer:
            return False
        # Prevent user from just copying the equation
        for sol in self.answer:
            if len(sol.atoms(sympy.Symbol)):
                return False
        solution = sympy.solveset(self.equation, self.x)
        sol_count = len(solution.args)
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
                self.name = str(uuid.uuid1())


def test_equation():
    assert isinstance(Equation(equation="x^2 - 5x + 6").solution, list)
    assert isinstance(Equation(equation="x^3 - 5x^2 + 6x").solution, list)
    assert isinstance(Equation(equation="x(x-1)(x-2)(x-3)").solution, sympy.FiniteSet)
    assert isinstance(Equation(equation="sin(x)").solution, sympy.Union)
