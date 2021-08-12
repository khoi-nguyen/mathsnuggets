"""
======
Plots
======
"""
import sympy

from mathsnuggets.core import fields, form

test = {"functions": "sin x"}


class Plot(form.Form):
    """Plot functions"""

    functions = fields.ExpressionList("Functions", required=True)
    x = fields.Expression("Variable", default="x")
    x_min = fields.Expression("x min", default="-10")
    x_max = fields.Expression("x max", default="10")
    y_min = fields.Expression("y min", default="-10")
    y_max = fields.Expression("y max", default="10")

    template = """
        <widget-settings>
            <config-option name="Functions">`functions`</config-option>
            <config-option name="x min">`x_min`</config-option>
            <config-option name="x max">`x_max`</config-option>
            <config-option name="y min">`y_min`</config-option>
            <config-option name="y max">`y_max`</config-option>
        </widget-settings>
        `plot`
    """

    @fields.computed("Plot", field=fields.Html, nohide=True)
    @fields.figure
    def plot(self):
        """Use SymPy/matplotlib to generate an SVG graph"""
        data = (self.x, self.x_min, self.x_max)
        graph = sympy.plot(*self.functions, data, show=False, ylabel="y")
        colors = [False, "red", "green", "orange"]
        for index in range(len(self.functions)):
            if index < len(colors) and colors[index]:
                graph[index].line_color = colors[index]
        backend = graph.backend(graph)
        backend.matplotlib.use("agg")
        backend.process_series()
        backend.fig.tight_layout()
        ax = backend.ax[0]
        ax.set_ylim([float(self.y_min), float(self.y_max)])
        ax.grid(True)
