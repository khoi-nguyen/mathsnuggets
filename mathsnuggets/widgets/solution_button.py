from mathsnuggets.core import fields, form


class SolutionButton(form.MarkedForm):
    """Solution button"""

    answer = fields.Markdown("Answer", required=True, setting=True)
    template = """
        `answer_button`
    """


    @fields.computed("Answer", field=fields.Markdown)
    def answer_button(self):
        return self.answer
