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
    x_min = fields.Expression("x min", default="-10", numeric=True)
    x_max = fields.Expression("x max", default="10", numeric=True)
    y_min = fields.Expression("y min", default="-10", numeric=True)
    y_max = fields.Expression("y max", default="10", numeric=True)
    height = fields.Expression("Height", default="5", numeric=True)
    ratio = fields.Expression("Ratio", default="1", numeric=True)

    template = """
        <widget-settings>
            ~functions~
            ~x_min~
            ~x_max~
            ~y_min~
            ~y_max~
            ~height~
            ~ratio~
        </widget-settings>
        `plot`
    """

    @property
    def width(self):
        return float(
            (self.x_max - self.x_min)
            / self.ratio
            * self.height
            / (self.y_max - self.y_min)
        )

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
        backend.fig.set_size_inches(self.width, self.height)
        ax = backend.ax[0]
        ax.set_ylim([self.y_min, self.y_max])
        ax.grid(True)
