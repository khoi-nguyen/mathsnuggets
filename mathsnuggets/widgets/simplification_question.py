import uuid

import sympy

from mathsnuggets.core import fields, form


class SimplificationQuestion(form.Form):
    """Simplification Question"""

    name = fields.Field("Survey name")
    answer = fields.Expression("Your answer", nosave=True, editable=True)
    expression = fields.Expression("Expression")

    template = """
        <div>Simplify `expression`</div>
        <survey
            :config="config"
            :name="payload.name"
            :showStats="loggedIn"
            :correct="computed.correct"
            :value="payload.answer">
            Your answer: `answer`
        </survey>
    """

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        if not self.answer:
            return False
        return str(self.answer) == str(sympy.simplify(self.expression))

    def validate(self):
        if not self.name:
            self.name = str(uuid.uuid1())
