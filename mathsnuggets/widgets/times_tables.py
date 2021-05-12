import random

import sympy

from mathsnuggets.core import fields, form


class TimesTables(form.Form):
    """Times tables"""

    table = fields.ExpressionList("Multiplication table", nosave=True)
    cols = fields.ExpressionList("Columns", default="2, 3, 4, 5, 6, 7, 8, 9, 11, 12")
    rows = fields.ExpressionList("Rows", default="2, 3, 4, 5, 6, 7, 8, 9, 11, 12")

    x = fields.RandomNumber("x")

    _total_marks = 100

    @property
    def _marks(self):
        return self.marking.count(1)

    @property
    def template(self):
        default = "0," * 99 + "0"
        cols_default = dict(getattr(type(self), "cols"))["default"]
        rows_default = dict(getattr(type(self), "rows"))["default"]
        return f"""
            <ul v-if="config.edit">
                <li>Cols: `cols`</li>
                <li>Rows: `rows`</li>
            </ul>
            <times-table
                :config="config"
                :value="payload.table || '{default}'"
                :cols="payload.cols || '{cols_default}'"
                :rows="payload.rows || '{rows_default}'"
                :marking="computed.marking"
                :size="10"
                @input="$set(payload, 'table', $event)"
                />
        """

    @fields.computed("Marking", fields.ExpressionList, nohide=True)
    def marking(self):
        marks = []
        for i, row in enumerate(self.rows):
            for j, col in enumerate(self.cols):
                pos = i * 10 + j
                value = 0
                if self.table is None or pos > len(self.table):
                    pass
                elif self.table[pos] == row * col:
                    value = 1
                elif self.table[pos]:
                    value = -1
                marks.append(value)
        return marks

    @fields.computed("Number of mistakes", fields.Expression, nohide=True)
    def mistakes_count(self):
        return self.marking.count(-1)

    def generator(self):
        possibilities = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.cols = random.sample(possibilities, 10)
        self.rows = random.sample(possibilities, 10)
        self.table = "0," * 99 + "0"
