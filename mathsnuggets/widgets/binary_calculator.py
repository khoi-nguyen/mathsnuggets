from mathsnuggets.core import fields, form

class BinaryCalculator(form.MarkedForm):
    """Binary Calculator"""

    base = fields.Expression("Base", default="2")
    bits = fields.Expression("Bits", default="4")
    show_decimal = fields.Boolean("Show decimal", default=True)
    template = """
        <widget-settings>
        ~base~ ~bits~ ~show_decimal~
        </widget-settings>
        <binary-converter :base="parseInt(payload.base)" :bits="parseInt(payload.bits)"
          :show-decimal="payload.show_decimal">
    """
