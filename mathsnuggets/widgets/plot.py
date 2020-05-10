"""
======
Plots
======
"""
import io

import sympy

from mathsnuggets.core import fields, form


class Plot(form.Form):
    """Plot functions"""

    function = fields.RealNumber("Function")
    x = fields.RealNumber("Variable", default="x")
    x_min = fields.RealNumber("x min", default="-10")
    x_max = fields.RealNumber("x max", default="10")

    template = """
        Plot `function` for `x` between `x_min` and `x_max`

        `plot`
    """

    @fields.computed("Plot", latex=False)
    def plot(self):
        """Use SymPy/matplotlib to generate an SVG graph"""
        data = (self.x, self.x_min, self.x_max)
        graph = sympy.plot(self.function, data, show=False)
        backend = graph.backend(graph)
        backend.matplotlib.use("svg")
        backend.process_series()
        backend.fig.tight_layout()
        tmp = io.BytesIO()
        backend.fig.savefig(tmp, format="svg")
        tmp.seek(0)
        svg = tmp.getvalue().decode("utf-8")
        return svg
