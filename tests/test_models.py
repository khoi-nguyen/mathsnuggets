import pytest

from mathsnuggets.core import db, models


@pytest.fixture
def mock_mongo(mongodb, monkeypatch):
    monkeypatch.setattr(db, "collections", mongodb)


def test_user(mock_mongo):
    assert db.collections.users.count_documents({}) == 1
    user = models.User()
    user.email = "test@test.com"
    user.password = "hellohello"
    assert user.password != "hellohello"
    assert user.check_password("hellohello")
    assert not user.check_password("foobar")
    assert user.get_id() is None

    user.save()
    assert db.collections.users.count_documents({}) == 2

    export = dict(user)
    assert not [k for k in export.keys() if k.startswith("_")]

    assert not db.collections.users.count_documents({"admin": True})
    user2 = models.User(email="test@test.com")
    user2.admin = True
    assert not isinstance(user2._id, str)
    assert isinstance(user2.get_id(), str)
    user2.save()
    assert db.collections.users.count_documents({"admin": True})
