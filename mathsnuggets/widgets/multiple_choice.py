import uuid

from mathsnuggets.core import fields, form


class MultipleChoice(form.Form):
    """Multiple Choice"""

    name = fields.Field("Survey name")
    answer = fields.Select("Your answer", nosave=True, options=["", "A", "B", "C", "D"])
    correct_answer = fields.Select("Correct Answer", options=["A", "B", "C", "D"])

    option_a = fields.Markdown("Option A")
    option_b = fields.Markdown("Option B")
    option_c = fields.Markdown("Option C")
    option_d = fields.Markdown("Option D")

    @property
    def template(self):
        buttons = []
        for ltr in ["a", "b", "c", "d"]:
            buttons.append(
                f"""
                <span v-if="!config.edit">
                    <b-button @click="$set(payload, 'answer', '{ltr.upper()}')"
                        type="is-primary"
                        v-if="'{ltr.upper()}' === payload.answer">
                        `option_{ltr}`
                    </b-button>
                    <b-button @click="$set(payload, 'answer', '{ltr.upper()}')" v-else>
                        `option_{ltr}`
                    </b-button>
                </span>
                <span v-else>
                    <b-button>`option_{ltr}`</b-button>
                </span>
            """
            )
        return f"""
            <ul v-if="config.edit">
                Correct answer: `correct_answer`
            </ul>
            <div class="container buttons are-large">
                {"".join(buttons)}
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
