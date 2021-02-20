"""
=======
Youtube
=======
"""
from mathsnuggets.core import fields, form

test = {"url": "https://www.youtube.com/watch?v=3d6DsjIBzJ4"}


class Youtube(form.Form):
    """YouTube"""

    name = "YouTube"
    url = fields.Field("URL")
    zoom = fields.Expression("Zoom", default="1.0")
    template = """
        <div v-if="config.edit">
            URL: `url`
            Zoom: `zoom`
        </div>
        `video`
    """

    @property
    def height(self):
        return 315 * self.zoom

    @property
    def width(self):
        return 560 * self.zoom

    @fields.computed("Youtube Video", field=fields.Html, nohide=True)
    def video(self):
        """Get HTML code of embedded YouTube video"""
        url = self.url.replace("watch?v=", "embed/")
        return f"""
            <iframe width="{self.width}" height="{self.height}"
                src="{url}" frameborder="0"
                allow="autoplay; encrypted-media" allowfullscreen>
            </iframe>
        """
