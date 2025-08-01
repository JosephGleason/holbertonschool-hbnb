#!/usr/bin/python3

from app.models.user import User

def test_user_creation():
    user = User(first_name="Jane", last_name="Doe", email="jane.doe@example.com")
    assert user.first_name == "Jane"
    assert user.last_name == "Doe"
    assert user.email == "jane.doe@example.com"
    assert user.is_admin is False
    print("test_user_creation passed!")

test_user_creation()
