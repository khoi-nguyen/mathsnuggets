from matplotlib import pyplot
import sympy

from mathsnuggets.core import fields, form


class PieChart(form.Form):
    """Pie Chart"""
    labels = fields.StringList("Labels", required=True)
    data = fields.ExpressionList("Data", required=True)
    size = fields.Expression("Figure size", default="6.4", numeric=True)
    template = """
        <widget-settings>
            <config-option name="labels">`labels`</config-option>
            <config-option name="Data">`data`</config-option>
            <config-option name="Size">`size`</config-option>
        </widget-settings>
        `pie_chart`
    """

    @fields.computed("Pie chart", field=fields.Html, nohide=True)
    @fields.figure
    def pie_chart(self):
        fig, ax = pyplot.subplots()
        ax.pie(self.data, shadow=True, labels=self.labels, autopct="%1.1f%%")
        ax.axis('equal')
        fig.set_size_inches(self.size, self.size)
