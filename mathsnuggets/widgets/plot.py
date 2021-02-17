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
    equal_aspect = fields.Boolean("Equal aspect", default=True)

    template = """
        <div v-if="config.edit">
            Plot `functions` for `x` between `x_min` and `x_max`
        </div>
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
        if self.equal_aspect:
            ax.axis("tight")
            ax.set_aspect("equal")
        ax.grid(True)
