import bson.objectid

from mathsnuggets.core import models

user = models.User()


def test_user():
    user.email = "test@test.com"
    user.password = "hellohello"
    assert user.password != "hellohello"
    assert user.check_password("hellohello")
    assert not user.check_password("foobar")
    assert user.get_id() is None

    user._id = bson.objectid.ObjectId()
    assert not isinstance(user._id, str)
    assert isinstance(user.get_id(), str)

    export = dict(user)
    assert not [k for k in export.keys() if k.startswith("_")]
