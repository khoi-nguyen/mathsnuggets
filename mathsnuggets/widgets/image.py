import base64
import hashlib
import mimetypes
import os

import PIL

from mathsnuggets.core import fields, form


class Image(form.Form):
    """Image"""

    src = fields.Field("Image URL", required=True)
    height = fields.Expression("Original height", default=0)
    width = fields.Expression("Original width", default=0)
    zoom = fields.Expression("Zoom", default=1, setting=True)
    position = fields.Select(
        "Position", options=["left", "right", "center"], default="center", setting=True
    )

    template = "`image`"

    @fields.computed("Image", field=fields.Html, nohide=True)
    def image(self):
        style = f"float:{self.position}" if self.position != "center" else ""
        return f"""
            <img src="{self.src}"
                width="{self.zoom * self.width}"
                style="{style}"
                height="{self.zoom * self.height}"/>"""

    def validate(self):
        if "," in self.src:
            data = self.src.split(",")
            image_hash = hashlib.sha1(data[1].encode("utf-8")).hexdigest()
            ext = mimetypes.guess_extension(data[0][5 : data[0].find(";")])
            folder = os.environ.get("STORAGE", "./storage/")
            filename = image_hash + ext
            with open(folder + filename, "wb") as f:
                image = base64.b64decode(data[1])
                f.write(image)
            self.src = "/storage/" + filename
        if not self.width:
            path = os.environ.get("STORAGE", "./storage/") + self.src[9:]
            self.width, self.height = PIL.Image.open(path).size
            self.zoom = 1
