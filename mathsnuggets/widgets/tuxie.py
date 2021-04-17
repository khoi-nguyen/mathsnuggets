from mathsnuggets.core import fields, form


class Tuxie(form.Form):
    """Tuxie says"""

    text = fields.Markdown("Text")
    width = fields.Expression("Tuxie width", default="400")

    template = """
        <div v-if="config.edit">
            Width: `width`
        </div>
        <tuxie :width="payload.width">`text`</tuxie>
    """
