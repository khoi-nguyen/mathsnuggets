from matplotlib import pyplot

from mathsnuggets.core import fields, form


class PieChart(form.Form):
    """Pie Chart"""

    data = fields.CSVData("Data", required=True)
    size = fields.Expression("Figure size", default="6.4", numeric=True)
    template = """
        <widget-settings>
            ~data~
            ~size~
        </widget-settings>
        `pie_chart`
    """

    @fields.computed("Pie chart", field=fields.Html, nohide=True)
    @fields.figure
    def pie_chart(self):
        fig, ax = pyplot.subplots()
        ax.pie(self.data[1], shadow=True, labels=self.data[0], autopct="%1.1f%%")
        ax.axis("equal")
        fig.set_size_inches(self.size, self.size)
