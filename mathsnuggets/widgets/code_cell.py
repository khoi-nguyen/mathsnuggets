from mathsnuggets.core import fields, form

class CodeCell(form.Form):
    """Code Cell"""

    template = """
        <div v-if="config.edit">`code`</div>
        <pre
           :data-executable="true"
           :data-language="payload.language || 'python'">{{ payload.code }}</pre>
    """

    language = fields.Field("Programming language", default="python")
    code = fields.Field("Code")
