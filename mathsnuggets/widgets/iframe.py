from mathsnuggets.core import fields, form


class Iframe(form.Form):
    """Iframe"""

    url = fields.Field("URL", required=True, setting=True)
    width = fields.Field("Width", default="90%", setting=True)
    height = fields.Field("Height", default="875", setting=True)

    template = "`iframe`"

    @fields.computed("Iframe", field=fields.Html, nohide=True)
    def iframe(self):
        return f"""
            <iframe
                width="{self.width}"
                height="{self.height}"
                src="{self.url}">
            </iframe>
        """
