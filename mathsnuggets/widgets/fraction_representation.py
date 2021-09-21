import sympy

from mathsnuggets.core import fields, form


def parse_fraction(expression):
    if expression == 1:
        return [1, 1]
    if expression.func == sympy.Pow:
        return [1, expression]
    return expression.args


class FractionRepresentation(form.Form):
    """Fraction representation"""

    fraction_1 = fields.Expression("Fraction (horizontal)", default="1")
    fraction_2 = fields.Expression("Fraction (vertical)", default="1")
    height = fields.Expression("Figure height", default="360")
    width = fields.Expression("Figure width", default="360")

    template = """
        <widget-settings>
            ~fraction_1~
            ~fraction_2~
            ~width~
            ~height~
        </widget-settings>
        `figure`
    """

    @fields.computed("Figure", field=fields.Html, nohide=True)
    def figure(self):
        num1, den1 = parse_fraction(self.fraction_1)
        num2, den2 = parse_fraction(self.fraction_2)
        x_inc, y_inc = sympy.floor(self.width * den2), sympy.floor(self.height * den1)
        x_inc, y_inc = int(x_inc), int(y_inc)
        lines = [
            (k, 0, k, self.height) for k in range(0, self.width + x_inc, x_inc)
        ] + [(0, k, self.width, k) for k in range(0, self.height + y_inc, y_inc)]
        lines = [
            f"""<line x1="{c[0]}" y1="{c[1]}" x2="{c[2]}" y2="{c[3]}" """
            + """style="stroke:#333333;stroke-width:2" />"""
            for c in lines
        ]
        return f"""
            <svg height="{self.height}" width="{self.width}">
            <rect x="0" y="0" style="fill:#255994;opacity:0.5"
                width="{self.fraction_2 * self.width}"
                height="{self.height}" />
            <rect x="0" y="0" style="fill:#2e6b53;opacity:0.5"
                width="{self.width}"
                height="{self.fraction_1 * self.height}" />
                {"".join(lines)}
            </svg>
        """
