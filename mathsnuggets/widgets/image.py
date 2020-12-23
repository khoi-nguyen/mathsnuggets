import base64
import hashlib
import mimetypes
import os

from mathsnuggets.core import fields, form


class Image(form.Form):
    """Image"""

    src = fields.Field("Image URL", required=True)
    template = """`image`"""

    @fields.computed("Image", field=fields.Html, nohide=True)
    def image(self):
        return f"""<img src="{self.src}" />"""

    def validate(self):
        if "," in self.src:
            data = self.src.split(",")
            image_hash = hashlib.sha1(data[1].encode("utf-8")).hexdigest()
            ext = mimetypes.guess_extension(data[0][5 : data[0].find(";")])
            folder = os.environ.get("STORAGE", "./storage/")
            filename = image_hash + ext
            with open(folder + filename, "wb") as f:
                f.write(base64.b64decode(data[1]))
            self.src = "/storage/" + filename
