import copy

from mathsnuggets import widgets
from mathsnuggets.core import db, fields


class Model:
    """Basic Model

    Instances of this class are meant to represent a MongoDB document.
    This class provides useful methods to find, update, and insert new entries.

    When creating an instance, keyword arguments may be supplied
    to load a specific document from the database.

    Example
    -------

    If there is a user with `test@test.com` as an email address,
    then the following will load it from the database.
    Otherwise, it will simply be a new MongoDB document
    that may be saved later.

    >>> user = User(email="test@test.com")
    >>> user.email
    >>> # Either 'test@test.com' if such a user exists or None

    Parameters
    ----------
    **query : dict
        MongoDB Query (as keyword arguments)

    Attributes
    ----------
    _id : ObjectId
        MongoDB Id of the record (``None`` if it's a new element)
    _collection :
        Relevant MongoDB collection
    """

    _id = fields.ObjectId("MongoDB ID")
    _collection = None

    def __init__(self, **query):
        if "_id" in query and query["_id"]:
            self._id = query["_id"]
            query["_id"] = self._id
        data = self._collection.find_one(query)
        if not data or not query:
            return None
        for attr, val in data.items():
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
        """Iterate through all relevant documents in the collection

        This is a **class** method.

        Parameters
        ----------
        *args:
            Supplied to PyMongo's ``find``
        **kwargs:
            Supplied to PyMongo's ``find``

        Yields
        ------
        Model
            An object form of a document satsifying the query

        Example
        -------
        The following example will change the password of all users to ``hellohello`.

        >>> for user in User.find({}):
        ...     user.password = 'hellohello'

        """
        for document in db.collections[cls._collection].find(*args, **kwargs):
            yield cls(_id=document["_id"])

    def update(self, patch, save=True):
        """Update the current document

        This will typically be used with a payload.

        Example
        -------

        Suppose we are working with a slideshow.

        >>> slideshow = Slideshow(title="Hello")

        Using ``update`` like the following

        >>> slideshow.update({"title": "New title", "slides.0.title": "Slide title"})

        is simply a shorthand for:

        >>> slideshow.title = "New title"
        >>> slideshow.slides[0]["title"] = "Slide title"
        >>> slideshow.save()

        Parameters
        ----------
        patch: dict
            Modifications to apply to the document
            (MongoDB's dot syntax is supported)
        save: bool
            Whether to save the document in the database afterwards
        """
        for attr, val in patch.items():
            obj = self
            for key in attr.split(".")[:-1]:
                if isinstance(obj, list):
                    obj = obj[int(key)]
                elif isinstance(obj, dict):
                    obj = obj[key]
                else:
                    obj = getattr(obj, key)
            key = attr.split(".")[-1]
            if isinstance(obj, list):
                obj[int(key)] = val
            elif isinstance(obj, dict):
                obj[key] = val
            else:
                setattr(obj, key, val)
        if save:
            self.save()

    def save(self):
        """Save the document in the collection

        - If the record exists, we update it.
        - Otherwise, we create a new one.
        """
        if self._id:
            self._collection.update_one({"_id": self._id}, {"$set": dict(iter(self))})
        else:
            doc = self._collection.insert_one(dict(iter(self)))
            self._id = doc.inserted_id


class Slideshow(Model):
    """Slideshow model

    This model aims to represent a slideshow.

    Attributes
    ----------
    title : str
        Title of the whole slideshow
    authors :
        Authors (format to be determined)
    slides : list
        Slides exactly as they are stored in the database
        (i.e. without the solutions or the fields' data).
    _slides : list
        Slides exactly as they should be sent to the frontend
        (with the computed fields and the fields' data).
    """

    _collection = db.collections.slideshows

    title = fields.Field("Title")
    authors = fields.Field("Authors")
    slides = [{"title": ""}]

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

    _collection = db.collections.users

    email = fields.Email("email")
    password = fields.Password("password")

    is_active = True
    is_authenticated = True
    is_anonymous = False

    def get_id(self):
        return str(self._id) if self._id else None

    def check_password(self, password):
        return type(self).password.check(password, self.password)
