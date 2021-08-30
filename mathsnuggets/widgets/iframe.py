from mathsnuggets.core import fields, form

class Iframe(form.Form):
    """Iframe"""

    url = fields.Field("URL", required=True)
    width = fields.Field("Width", default="90%")
    height = fields.Field("Height", default="600")

    template = """
        <widget-settings>
            ~url~
            ~width~
            ~height~
        </widget-settings>
        `iframe`
    """

    @fields.computed("Iframe", field=fields.Html, nohide=True)
    def iframe(self):
        return f"""
            <iframe
                width="{self.width}"
                height="{self.height}"
                src="{self.url}">
            </iframe>
        """
