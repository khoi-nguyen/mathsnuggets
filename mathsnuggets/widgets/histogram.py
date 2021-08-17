from matplotlib import pyplot

from mathsnuggets.core import fields, form

class Histogram(form.Form):
    """Histogram"""

    data = fields.CSVData("Data", required=True)
    size = fields.Expression("Figure size", default="6.4", numeric=True)
    template = """
        <widget-settings>
            ~data~
            ~size~
        </widget-settings>
        `histogram`
    """

    @fields.computed("Histogram", field=fields.Html, nohide=True)
    @fields.figure
    def histogram(self):
        bins = [r[0] for r in self.data]
        bins.append(self.data[-1][1])
        x = []
        for left, right, frequency in self.data:
            x += [left] * int(frequency)
        pyplot.hist(x, density=True, bins=bins)
