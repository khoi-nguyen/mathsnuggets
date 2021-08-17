from matplotlib import pyplot

from mathsnuggets.core import fields, form


class BarChart(form.Form):
    """Bar Chart"""

    data = fields.CSVData("Data", required=True)
    size = fields.Expression("Figure size", default="6.4", numeric=True)
    template = """
        <widget-settings>
            ~data~
            ~size~
        </widget-settings>
        `bar_chart`
    """

    @fields.computed("Bar chart", field=fields.Html, nohide=True)
    @fields.figure
    def bar_chart(self):
        fig, ax = pyplot.subplots()
        ax.bar(self.data[0], self.data[1])
        fig.set_size_inches(self.size, self.size)
