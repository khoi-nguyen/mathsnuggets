import uuid

from mathsnuggets.core import fields, form


class Survey(form.Form):
    """Survey"""

    name = fields.Field("Survey name")
    answer = fields.Expression("Your answer", nosave=True)
    correct_answer = fields.Expression("Correct Answer")

    template = """
        <p>Your answer: `answer`</p>
        <div v-if="config.edit">
            <p>Correct answer: `correct_answer`</p>
        </div>
        <survey
            :name="payload.name"
            :showStats="config.authState.loggedIn"
            :correct="computed.correct"
            :value="payload.answer"
        />
    """

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        return self.answer == self.correct_answer

    def validate(self):
        if not self.name:
            self.name = str(uuid.uuid1())
