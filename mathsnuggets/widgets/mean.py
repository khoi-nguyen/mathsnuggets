import statistics

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
        if self.data:
            total = sum([row[-1] for row in self.data])
            return (
                sum([statistics.mean(row[:-1]) * row[-1] for row in self.data]) / total
            )
        elif self.numbers:
            return statistics.mean(self.numbers)


def test_mean():
    assert Mean(numbers="1,2,3,4,5").mean == 3
    assert Mean(data="1,2\n2,3\n4,1").mean == 2
