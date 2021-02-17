import uuid

import sympy

from mathsnuggets.core import fields, form


class StandardFormQuestion(form.Form):
    """Standard form question"""

    name = fields.Field("Survey name")
    answer = fields.Expression("Your answer", nosave=True, editable=True)
    expression = fields.Expression("Expression")

    template = """
        <p>Convert `expression` to standard form</p>
        <survey
            :name="payload.name"
            :showStats="config.authState.loggedIn"
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
            if self.answer.args[0] != 10:
                return False
        else:
            if self.answer.func != sympy.Mul or len(self.answer.args) != 2:
                return False
            x, power = self.answer.args[0], self.answer.args[1]
            if (
                x not in sympy.Interval.Ropen(1, 10)
                or power.func != sympy.Pow
                or power.args[0] != 10
            ):
                return False
        return sympy.simplify(self.answer - self.expression) == 0

    def validate(self):
        if not self.name:
            self.name = str(uuid.uuid1())
