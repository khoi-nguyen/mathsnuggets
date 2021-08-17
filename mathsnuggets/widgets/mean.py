import statistics

import sympy

from mathsnuggets.core import fields, form
from mathsnuggets.widgets import table


class Mean(form.Form):
    """Mean"""

    template = """
        Find the mean of
        <span v-if="config.edit || payload.numbers">`numbers`</span>
        <span v-if="config.edit">`data`</span>
        <div v-if="payload.data">`frequency_table`</div>
        `mean`
    """
    data = fields.CSVData("Numbers")
    numbers = fields.NumberList("Numbers")

    @fields.computed("Table", field=fields.Html, nohide=True)
    def frequency_table(self):
        if not self.data:
            return ""
        thead = [""] * (len(self.data[0]) - 1) + ["Frequency"]
        return table.Table(data=[thead] + self.data).table

    @fields.computed("Mean")
    def mean(self):
        if self.data and len(self.data[0]) == 2:
            total = sum([row[1] for row in self.data])
            return sum([f * x for x, f in self.data]) / total
        elif self.data and len(self.data[0]) == 3:
            total = sum([row[2] for row in self.data])
            return sum([(l + r) / 2 * f for l, r, f in self.data]) / total
        elif self.numbers:
            return statistics.mean(self.numbers)
