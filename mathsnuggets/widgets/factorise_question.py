import uuid

import sympy

from mathsnuggets.core import fields, form


class FactoriseQuestion(form.Form):
    """Factorisation Question"""

    name = fields.Field("Survey name")
    answer = fields.Expression("Your answer", nosave=True, editable=True)
    expression = fields.Expression("Expression")

    template = """
        <p>Factorise `expression`</p>
        <survey
            :name="payload.name"
            :showStats="config.authState.loggedIn"
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
        if not self.name:
            self.name = str(uuid.uuid1())
