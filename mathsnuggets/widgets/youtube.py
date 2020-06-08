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
    template = """`url` `video`"""

    @fields.computed("Youtube Video", field=fields.Html)
    def video(self):
        """Get HTML code of embedded YouTube video"""
        url = self.url.replace("watch?v=", "embed/")
        return f"""
            <iframe width="560" height="315" src="{url}" frameborder="0"
                allow="autoplay; encrypted-media" allowfullscreen>
            </iframe>
        """
