from mathsnuggets.core import fields, form

class BinaryAdder(form.Form):
    """Binary adder"""

    bits = fields.Expression("Bits", default="8")
    template = """
        <widget-settings>
        ~bits~
        </widget-settings>
        <binary-adder :bits="parseInt(payload.bits) || 8">
    """
