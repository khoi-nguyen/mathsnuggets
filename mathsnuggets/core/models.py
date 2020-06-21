import copy

from mathsnuggets import widgets
from mathsnuggets.core import db, fields


class Model:
    _use_setter = []

    _id = fields.ObjectId("MongoDB ID")

    def __init__(self, **query):
        if "_id" in query and query["_id"]:
            self._id = query["_id"]
            query["_id"] = self._id
        data = db.collections[self._collection].find_one(query)
        if not data or not query:
            return None
        for attr, val in data.items():
            if attr in self._use_setter:
                setattr(self, attr, val)
            else:
                self.__dict__[attr] = val

    def __iter__(self):
        if self._id:
            yield ("id", str(self._id))
        for attr in dir(self):
            value = getattr(self, attr)
            if not attr.startswith("_") and not callable(value):
                yield (attr, value)

    @classmethod
    def find(cls, *args, **kwargs):
        for document in db.collections[cls._collection].find(*args, **kwargs):
            yield cls(_id=document["_id"])

    def save(self):
        if self._id:
            db.collections[self._collection].update_one(
                {"_id": self._id}, {"$set": dict(iter(self))}
            )
        else:
            doc = db.collections[self._collection].insert_one(dict(iter(self)))
            self._id = doc.inserted_id


class Slideshow(Model):
    _use_setter = ["slides"]
    _collection = "slideshows"

    slides = [{"title": ""}]

    title = fields.Field("Title")
    authors = fields.Field("Authors")

    @property
    def _slides(self):
        slides = copy.deepcopy(self.slides)
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
        return slides


class User(Model):

    _collection = "users"

    email = fields.Email("email")
    password = fields.Password("password")

    is_active = True
    is_authenticated = True
    is_anonymous = False

    def get_id(self):
        return str(self._id) if self._id else None

    def check_password(self, password):
        return type(self).password.check(password, self.password)
