import sympy

from mathsnuggets.core import fields, form


class FactoriseQuestion(form.Form):
    """Factorisation Question"""

    answer = fields.Expression("Your answer", nosave=True, editable=True)
    expression = fields.Expression("Expression", required=True)

    template = """
        <div>Factorise `expression`</div>
        <survey
            :name="payload.name"
            :correct="computed.correct"
            :value="payload.answer">
            Your answer: `answer`
        </survey>
    """

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if (
            not self.answer
            or sympy.simplify(self.answer - self.expression) != 0
            or self.answer.func != sympy.Mul
        ):
            return False
        for term in self.answer.args:
            if sympy.factor(term).func == sympy.Mul:
                return False
        return True

    def validate(self):
        self.expression = sympy.expand(self.expression)
        super().validate()
