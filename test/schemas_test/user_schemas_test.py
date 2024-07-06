import unittest
from datetime import date

from pydantic import EmailStr, ValidationError

import app
from app.schemas.users_schemas.users import (
    User,
    UserBase,
    UserCreate,
    UserId,
    UserLogin,
)


class TestUserModels(unittest.TestCase):

    def test_user_base(self):
        user_base = UserBase(
            username="username",
            email="username@example.com",
            birth_date=date(1999, 10, 31),
            preferences=["Cafe"],
            city="Buenos Aires",
        )
        self.assertEqual(user_base.username, "username")
        self.assertEqual(user_base.email, "username@example.com")
        self.assertEqual(user_base.birth_date, date(1999, 10, 31))
        self.assertEqual(user_base.preferences, ["Cafe"])
        self.assertEqual(user_base.city, "Buenos Aires")

    def test_user_create(self):
        user_create = UserCreate(
            username="username",
            email="username@example.com",
            birth_date=date(1999, 10, 31),
            preferences=["Park"],
            city="Buenos Aires",
            password="password",
            fcm_token="valid_fcm_token",
        )
        self.assertEqual(user_create.username, "username")
        self.assertEqual(user_create.email, "username@example.com")
        self.assertEqual(user_create.birth_date, date(1999, 10, 31))
        self.assertEqual(user_create.preferences, ["Park"])
        self.assertEqual(user_create.city, "Buenos Aires")
        self.assertEqual(user_create.password, "password")
        self.assertEqual(user_create.fcm_token, "valid_fcm_token")

    def test_user_id(self):
        user_id = UserId(id=1)
        self.assertEqual(user_id.id, 1)

    def test_user(self):
        user = User(
            id=1,
            username="username",
            email="username@example.com",
            birth_date=date(1999, 10, 31),
            preferences=["Cafe"],
            city="Buenos Aires",
        )
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "username")
        self.assertEqual(user.email, "username@example.com")
        self.assertEqual(user.birth_date, date(1999, 10, 31))
        self.assertEqual(user.preferences, ["Cafe"])
        self.assertEqual(user.city, "Buenos Aires")

    def test_user_login(self):
        user_login = UserLogin(email="username@example.com", password="password")
        self.assertEqual(user_login.email, "username@example.com")
        self.assertEqual(user_login.password, "password")
