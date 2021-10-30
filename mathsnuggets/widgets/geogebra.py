"""
=======
Youtube
=======
"""
from mathsnuggets.core import fields, form

test = {"url": "https://www.geogebra.org/m/UjjwuM8p"}


class Geogebra(form.Form):
    """Geogebra"""

    name = "Geogebra"
    url = fields.Field("URL", required=True, setting=True)
    width = fields.Expression("Width", default=800, setting=True)
    height = fields.Expression("Height", default=600, setting=True)
    template = "`geogebra`"

    @fields.computed("Geogebra", field=fields.Html, nohide=True)
    def geogebra(self):
        """Get HTML code of embedded YouTube video"""
        url = self.url.split("/")[-1]
        url = f"https://www.geogebra.org/material/iframe/id/{url}"
        url += f"/width/{self.width}/height/{self.height}"
        url += "/ai/false/smb/false/stb/false"
        return f"""
          <iframe scrolling="no"
            src="{url}"
            height="{self.height}"
            width="{self.width}"
            style="border: 0px;" allowfullscreen>
          </iframe>
        """
