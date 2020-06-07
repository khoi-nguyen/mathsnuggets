import flask_login

from mathsnuggets.core import db, fields


class Model:
    def __init__(self, **query):
        if query:
            data = db.collections[self._collection].find_one(query)
            if data:
                for attr, val in data.items():
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


class User(Model, flask_login.UserMixin):

    _collection = "users"

    email = fields.Email("email")
    password = fields.Password("password")

    def check_password(self, password):
        return type(self).password.check(password, self.password)
