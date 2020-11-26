from mathsnuggets.core import fields, form


class Image(form.Form):
    """Image"""

    src = fields.Field("Image URL", required=True)
    template = """`image`"""

    @fields.computed("Image", field=fields.Html, nohide=True)
    def image(self):
        return f"""<img src="{self.src}" />"""
