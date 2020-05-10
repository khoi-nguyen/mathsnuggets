"""
======
Pandoc
======
"""
from mathsnuggets.core import fields, form


class Pandoc(form.Form):
    """Rich Text"""

    markdown = fields.Markdown("Markdown")
    template = "`markdown`"
