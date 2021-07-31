import sympy

from mathsnuggets.core import fields, form


class StandardForm(form.MarkedForm):
    """Standard form question"""

    answer = fields.Expression("Your answer", nosave=True, editable=True)
    expression = fields.Expression("Expression")

    template = """
        <p>Convert `expression` to standard form</p>
        <survey
            :name="payload.name"
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
        return sympy.simplify(self.answer - self.expression) == 0


def test_standard_form():
    assert StandardForm(expression="0.3", answer="3*10^-1")
    assert StandardForm(expression="0.3", answer="3E-1")
    assert StandardForm(expression="300", answer="3*10^2")
    assert StandardForm(expression="635", answer="6.35*10**2")
