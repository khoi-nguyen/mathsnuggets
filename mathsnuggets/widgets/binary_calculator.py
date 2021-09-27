import sympy

from mathsnuggets.core import fields, form

class BinaryCalculator(form.MarkedForm):
    """Binary Calculator"""

    base = fields.Expression("Base", default="2")
    bits = fields.Expression("Bits", default="4")
    template = """
        <widget-settings>
        ~base~ ~bits~
        </widget-settings>
        <binary-converter :base="parseInt(payload.base)" :bits="parseInt(payload.bits)">
    """
