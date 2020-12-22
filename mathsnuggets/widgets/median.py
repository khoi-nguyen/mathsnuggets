import statistics

from mathsnuggets.core import fields, form


class Median(form.Form):
    """Median"""

    template = "Find the median of `numbers` `median`"
    numbers = fields.NumberList("Numbers")

    @fields.computed("Median")
    def median(self):
        return statistics.median(self.numbers)
