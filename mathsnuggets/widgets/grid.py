from mathsnuggets.core import fields, form


class Grid(form.Form):
    """Grid"""

    x_min = fields.Expression("x min", default="-10")
    y_min = fields.Expression("y min", default="-10")
    x_max = fields.Expression("x max", default="10")
    y_max = fields.Expression("y max", default="10")
    x_inc = fields.Expression("x inc", default="50")
    y_inc = fields.Expression("y inc", default="50")

    template = """
        <div v-if="config.edit">
            <p>From (`x_min`, `y_min`) to (`x_max`, `y_max`)</p>
            <p>Square dimensions (px): `x_inc` x `y_inc`</p>
        </div>
        `grid`
    """

    @fields.computed("Grid", field=fields.Html, nohide=True)
    def grid(self):
        height = (self.y_max - self.y_min) * self.y_inc
        width = (self.x_max - self.x_min) * self.x_inc
        lines = [
            (k, 0, k, height) for k in range(0, width + self.x_inc, self.x_inc)
        ] + [(0, k, width, k) for k in range(0, height + self.x_inc, self.y_inc)]
        lines = [
            f"""<line x1="{c[0]}" y1="{c[1]}" x2="{c[2]}" y2="{c[3]}" """
            + """style="stroke:rgb(189,189,189);stroke-width:1" />"""
            for c in lines
        ]
        return f"""
            <svg height="{height}" width="{width}">
                <defs>
                    <marker id="arrowhead"
                        markerWidth="10" markerHeight="7"
                        refX="0" refY="3.5" orient="auto">
                        <polygon points="0 0, 10 3.5, 0 7" />
                    </marker>
                </defs>
                {"".join(lines)}
                <line x1="0" y1="{self.y_max * self.y_inc}"
                    x2="{width - self.x_inc/2}" y2="{self.y_max * self.y_inc}"
                    style="stroke:rgb(0, 0, 0);stroke-width:2"
                    marker-end="url(#arrowhead)" />
                <line x1="{-self.x_min * self.x_inc}" y2="{self.y_inc/2}"
                    x2="{-self.x_min * self.x_inc}" y1="{height}"
                    style="stroke:rgb(0, 0, 0);stroke-width:2"
                    marker-end="url(#arrowhead)" />
            </svg>
        """
