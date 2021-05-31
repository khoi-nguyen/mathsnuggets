from mathsnuggets.core import fields, form


class Tuxie(form.Form):
    """Tuxie says"""

    text = fields.Markdown("Text")
    width = fields.Expression("Tuxie width", default="400")
    image = fields.Select(
        "Image", options=["tuxie", "jigglypuff", "pikachu"], default="tuxie"
    )

    template = """
        <widget-settings v-if="config.edit">
            <config-option name="Image">`image`</config-option>
            <config-option name="Width">`width`</config-option>
        </widget-settings>
        <tuxie :width="payload.width" :image="payload.image">`text`</tuxie>
    """
