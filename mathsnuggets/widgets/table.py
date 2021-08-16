from mathsnuggets.core import fields, form


class Table(form.Form):
    "Table"

    data = fields.CSVData("Data", required=True)

    template = """
        <widget-settings>
            ~data~
        </widget-settings>
        `table`
    """

    @fields.computed("Table", field=fields.Html, nohide=True)
    def table(self):
        html = "<table class='table is-striped'>"
        for index, row in enumerate(self.data):
            html += "<tr>"
            for cell in row:
                if index == 0:
                    html += f"<th>{cell}</th>"
                else:
                    html += f"<td>{cell}</td>"
            html += "</tr>"
        html += "</table>"
        return html
