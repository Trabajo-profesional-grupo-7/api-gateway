import unittest
from datetime import datetime

from pydantic import EmailStr, ValidationError

import app
from app.schemas.users_schemas.password import (
    InitRecoverPassword,
    PasswordRecover,
    UpdatePassword,
    UpdateRecoverPassword,
)


class TestPasswordModels(unittest.TestCase):

    def test_update_password(self):
        update_password = UpdatePassword(
            current_password="old_password", new_password="new_password"
        )
        self.assertEqual(update_password.current_password, "old_password")
        self.assertEqual(update_password.new_password, "new_password")

    def test_password_recover(self):
        recover_time = datetime.now()
        password_recover = PasswordRecover(
            user_id=123, emited_datetime=recover_time, leftover_attempts=3
        )
        self.assertEqual(password_recover.user_id, 123)
        self.assertEqual(password_recover.emited_datetime, recover_time)
        self.assertEqual(password_recover.leftover_attempts, 3)

    def test_init_recover_password(self):
        init_recover_password = InitRecoverPassword(email="username@example.com")
        self.assertEqual(init_recover_password.email, "username@example.com")

    def test_update_recover_password(self):
        update_recover_password = UpdateRecoverPassword(
            email="username@example.com",
            code="recover_code",
            new_password="new_password",
        )
        self.assertEqual(update_recover_password.email, "username@example.com")
        self.assertEqual(update_recover_password.code, "recover_code")
        self.assertEqual(update_recover_password.new_password, "new_password")
