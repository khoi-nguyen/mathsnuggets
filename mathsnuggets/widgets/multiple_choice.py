import uuid

from mathsnuggets.core import fields, form

class MultipleChoice(form.Form):
    """Multiple Choice"""

    name = fields.Field("Survey name")
    answer = fields.Select("Your answer", nosave=True, options=["", "A", "B", "C", "D"])
    correct_answer = fields.Select("Correct Answer", options=["A", "B", "C", "D"])

    option_a = fields.Expression("Option A")
    option_b = fields.Expression("Option B")
    option_c = fields.Expression("Option C")
    option_d = fields.Expression("Option D")

    template = """
        <ul v-if="config.edit">
            Correct answer: `correct_answer`
        </ul>
        <div class="container buttons are-medium">
            <b-button>A: `option_a`</b-button>
            <b-button>B: `option_b`</b-button>
            <b-button>C: `option_c`</b-button>
            <b-button>D: `option_d`</b-button>
        </div>
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
        return self.answer == self.correct_answer

    def validate(self):
        if not self.name:
            self.name = str(uuid.uuid1())
