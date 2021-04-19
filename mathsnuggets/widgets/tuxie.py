from mathsnuggets.core import fields, form


class Tuxie(form.Form):
    """Tuxie says"""

    text = fields.Markdown("Text")
    width = fields.Expression("Tuxie width", default="400")
    image = fields.Select("Image", options=["tuxie", "jigglypuff", "pikachu"], default="tuxie")

    template = """
        <div v-if="config.edit">
            `image`
            Width: `width`
        </div>
        <tuxie :width="payload.width" :image="payload.image">`text`</tuxie>
    """
