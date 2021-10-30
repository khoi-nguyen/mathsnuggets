from mathsnuggets.core import fields, form


class BinaryCalculator(form.MarkedForm):
    """Binary Calculator"""

    base = fields.Expression("Base", default="2", setting=True)
    bits = fields.Expression("Bits", default="4", setting=True)
    show_decimal = fields.Boolean("Show decimal", default=True, setting=True)
    template = """
        <binary-converter :base="parseInt(payload.base)" :bits="parseInt(payload.bits)"
          :show-decimal="payload.show_decimal">
    """
