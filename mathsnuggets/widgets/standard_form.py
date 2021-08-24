import sympy

from mathsnuggets.core import fields, form, tools


class StandardForm(form.MarkedForm):
    """Standard form question"""

    answer = fields.Expression("Your answer", nosave=True, editable=True)
    expression = fields.Expression("Expression")

    template = """
        <p>Convert `expression` to standard form</p>
        <survey
            :correct="computed.correct"
            :value="payload.answer">
            `answer`
        </survey>
    """

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if not self.answer:
            return False
        if self.answer.func == sympy.Pow:
            if self.answer.args[0] != sympy.UnevaluatedExpr(10):
                return False
        else:
            if self.answer.func != sympy.Mul or len(self.answer.args) != 2:
                return False
            x, power = self.answer.args[0], self.answer.args[1]
            if (
                x not in sympy.Interval.Ropen(1, 10)
                or power.func != sympy.Pow
                or power.args[0] != sympy.UnevaluatedExpr(10)
            ):
                return False
        return tools.isequal(self.answer, self.expression)


def test_standard_form():
    assert StandardForm(expression="0.3", answer="3*10^-1").correct
    assert StandardForm(expression="0.3", answer="3E-1").correct
    assert StandardForm(expression="300", answer="3*10^2").correct
    assert StandardForm(expression="635", answer="6.35*10**2").correct
    assert StandardForm(expression="3401", answer="3.401*10^3").correct
