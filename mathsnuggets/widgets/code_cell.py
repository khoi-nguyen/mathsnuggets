import urllib

from mathsnuggets.core import fields, form

class CodeCell(form.Form):
    """Code Cell"""

    template = """
        <widget-settings>
            ~height~
        </widget-settings>
        <div v-if="config.edit">`code`</div>
        <div v-else>
            <iframe :src="computed.url" width="100%" :height="payload.height + 'px'">
            </iframe>
        </div>
    """

    language = fields.Field("Programming language", default="python", required=True)
    code = fields.Code("Code", required=True)
    height = fields.Field("Height", default="400")

    @fields.computed("Iframe URL", field=fields.Field, nohide=True)
    def url(self):
        return f"/jupyter/{self.language}?" + urllib.parse.urlencode({"code": self.code})
