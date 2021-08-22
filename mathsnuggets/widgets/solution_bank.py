import bs4
import requests

from mathsnuggets.core import fields, form


class SolutionBank(form.Form):
    """Solution bank"""

    book = fields.Select(
        "Book",
        required=True,
        options=[
            "pure-maths-year-1",
            "pure-maths-year-2",
            "statistics-mechanics-year-1",
            "statistics-mechanics-year-2",
            "core-pure-maths-1",
            "core-pure-maths-2",
            "further-pure-maths-1",
            "further-pure-maths-2",
            "further-statistics-1",
            "further-statistics-2",
            "further-mechanics-1",
            "further-mechanics-2",
            "decision-maths-1",
            "decision-maths-2",
        ],
    )
    exercise = fields.Field("Exercise", required=True)

    template = """
        <widget-settings>
            ~book~ ~exercise~
        </widget-settings>
        `link`
    """

    @property
    def scrap_url(self):
        return (
            "https://www.physicsandmathstutor.com/maths-revision/solutionbanks/edexcel-"
            + self.book
            + "/"
        )

    @fields.computed("Solution bank", field=fields.Html, nohide=True)
    def link(self):
        page = requests.get(self.scrap_url)
        if page.status_code != 200:
            raise ValueError(f"The book {self.book} does not exist")
        soup = bs4.BeautifulSoup(page.content, "html.parser")
        search = soup.body.find(text=self.exercise)
        if not search:
            raise ValueError(f"The exercise {self.exercise} cannot be found")
        url = search.parent.get("href")
        return f"""
            <a href="{url}" target="_blank">Solution {self.exercise}</a>
        """
