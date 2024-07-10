import unittest

from pydantic import ValidationError

import app
from app.schemas.users_schemas.autentication import Token


class TestTokenModel(unittest.TestCase):

    def test_token(self):
        token = Token(token="abc123", refresh_token="def456", token_type="Bearer")
        self.assertEqual(token.token, "abc123")
        self.assertEqual(token.refresh_token, "def456")
        self.assertEqual(token.token_type, "Bearer")
