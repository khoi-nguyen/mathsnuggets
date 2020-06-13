import flask_login

from mathsnuggets import widgets
from mathsnuggets.core import db, fields


class Model:
    _use_setter = []

    def __init__(self, **query):
        if query:
            data = db.collections[self._collection].find_one(query)
            if data:
                for attr, val in data.items():
                    if attr in self._use_setter:
                        setattr(self, attr, val)
                    else:
                        self.__dict__[attr] = val

    def __iter__(self):
        for attr in dir(self):
            value = getattr(self, attr)
            if not attr.startswith("_") and not callable(value):
                yield (attr, value)

    def get_id(self):
        if hasattr(self, "_id"):
            return str(self._id)
        return None

    def save(self):
        if hasattr(self, "_id"):
            db.collections[self._collection].update_one(
                {"_id": self._id}, {"$set": dict(iter(self))}
            )
        else:
            db.collections[self._collection].insert_one(dict(iter(self)))


class Slideshow(Model):
    _use_setter = ["slides"]
    _collection = "slideshows"
    _slides = [{"title": ""}]

    title = fields.Field("Title")
    authors = fields.Field("Authors")

    @property
    def slides(self):
        return self._slides

    @slides.setter
    def slides(self, slides):
        for slide in slides:
            if "widgets" not in slide:
                slide["widgets"] = [[{"type": "", "fields": []}]]
                continue
            for col in slide["widgets"]:
                for widget in col:
                    if "fields" not in widget:
                        continue
                    form = getattr(widgets, widget["type"])(**widget["fields"])
                    data = [f for n, f in form._fields()]
                    data.sort(key=lambda f: f.get("order"))
                    widget["fields"] = data
        self._slides = slides


class User(Model, flask_login.UserMixin):

    _collection = "users"

    email = fields.Email("email")
    password = fields.Password("password")

    def check_password(self, password):
        return type(self).password.check(password, self.password)
