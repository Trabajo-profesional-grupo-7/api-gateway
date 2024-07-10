import unittest
from unittest.mock import Mock, patch

from fastapi.security import HTTPAuthorizationCredentials

import app
from app.services.authentication_service import check_authentication, get_user_id
from app.utils.api_exception import APIException


class TestAuthenticationServices(unittest.TestCase):

    @patch("app.services.authentication_service.requests.get")
    def test_check_authentication_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        credentials_dict = {"scheme": "Bearer", "credentials": "valid_credentials"}
        credentials = HTTPAuthorizationCredentials(**credentials_dict)
        result = check_authentication(credentials)
        self.assertTrue(result)

    @patch("app.services.authentication_service.requests.get")
    def test_check_authentication_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        credentials_dict = {"scheme": "Bearer", "credentials": "invalid_credentials"}
        credentials = HTTPAuthorizationCredentials(**credentials_dict)
        with self.assertRaises(APIException):
            app.services.authentication_service.check_authentication(credentials)

    @patch("app.services.authentication_service.requests.get")
    def test_get_user_id_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = 1
        mock_get.return_value = mock_response

        credentials_dict = {"scheme": "Bearer", "credentials": "valid_credentials"}
        credentials = HTTPAuthorizationCredentials(**credentials_dict)
        user_id = app.services.authentication_service.get_user_id(credentials)
        self.assertEqual(user_id, 1)
