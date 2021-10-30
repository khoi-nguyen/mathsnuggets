from mathsnuggets.core import fields, form


class BinaryAdder(form.Form):
    """Binary adder"""

    bits = fields.Expression("Bits", default="8", setting=True)
    template = """<binary-adder :bits="parseInt(payload.bits) || 8">"""
