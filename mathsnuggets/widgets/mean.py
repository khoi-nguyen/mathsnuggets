import statistics

import sympy

from mathsnuggets.core import fields, form


class Mean(form.Form):
    """Mean"""

    template = "Find the mean of `numbers` `mean`"
    numbers = fields.NumberList("Numbers")

    @fields.computed("Mean")
    def mean(self):
        return statistics.mean(self.numbers)
