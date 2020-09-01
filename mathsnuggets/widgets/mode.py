import statistics

import sympy

from mathsnuggets.core import fields, form

class Mode(form.Form):
    """Mode"""

    template =  "Find the mode of `numbers` `mode`"
    numbers = fields.NumberList("Numbers")

    @fields.computed("Mode")
    def mode(self):
        return statistics.mode(self.numbers)
