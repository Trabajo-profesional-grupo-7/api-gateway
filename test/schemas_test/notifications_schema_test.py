import unittest
from unittest.mock import Mock, patch

import app
from app.schemas.notifications.token import FcmToken


class TestStoreFcmToken(unittest.TestCase):

    def test_store_fcm_token_success(self):
        token_data = {"fcm_token": "valid_fcm_token"}
        result = FcmToken(**token_data)

        self.assertIsInstance(result, FcmToken)
        self.assertEqual(result.fcm_token, "valid_fcm_token")
