"""
======
Pandoc
======
"""
from mathsnuggets.core import fields, form


class Pandoc(form.Form):
    """Rich text"""

    template = "`markdown`"

    markdown = fields.Markdown("Markdown")
