from mathsnuggets.core import fields, form


class MultipleChoice(form.MarkedForm):
    """Multiple Choice"""

    answer = fields.Select(
        "Your answer", nosave=True, options=["", "A", "B", "C", "D", "E"]
    )
    correct_answer = fields.Select(
        "Correct Answer", options=["A", "B", "C", "D", "E"], default="A", setting=True
    )
    question = fields.Markdown("Question")

    option_a = fields.Markdown("A")
    option_b = fields.Markdown("B")
    option_c = fields.Markdown("C")
    option_d = fields.Markdown("D")
    option_e = fields.Markdown("E")

    @property
    def template(self):
        buttons = []
        for ltr in ["a", "b", "c", "d", "e"]:
            buttons.append(
                f"""
                <span v-if="!config.edit">
                    <span v-if="payload.option_{ltr}">
                        <b-button @click="$set(payload, 'answer', '{ltr.upper()}')"
                            type="is-primary"
                            v-if="'{ltr.upper()}' === payload.answer">
                            `option_{ltr}`
                        </b-button>
                        <b-button
                            @click="$set(payload, 'answer', '{ltr.upper()}')"
                            v-else
                        >
                            `option_{ltr}`
                        </b-button>
                    </span>
                </span>
                <span v-else>
                   <b-button>`option_{ltr}`</b-button>
                </span>
            """
            )
        return f"""
            <p v-if="config.edit || payload.question">`question`</p>
            <survey
                :correct="computed.correct"
                :max-attempts="1"
                :value="payload.answer">
                <span class="buttons are-large">
                    {"".join(buttons)}
                </span>
            </survey>
    """

    @fields.computed("Correct", field=fields.Boolean)
    def correct(self):
        return self.answer == self.correct_answer
