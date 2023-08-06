import unittest
from unittest.mock import patch

import requests

import cobra.user
from cobra.utils.urls import BASE_URL


class TestUserAPI(unittest.TestCase):
    """Test user API."""
    def test_user_login(self):
        """Test user.login API."""
        with patch('builtins.input', return_value='!2345678'):
            self.assertIsNone(cobra.user._refresh_token)
            token = cobra.user.login('m@tum.de')
            self.assertIsNotNone(token)
            r = requests.post(BASE_URL + 'token/verify/', data={'token': token})
            self.assertEqual(r.status_code, 200)
            self.assertIsNotNone(cobra.user._refresh_token)
            token = cobra.user.login('m@tum.de')
            r = requests.post(BASE_URL + 'token/verify/', data={'token': token})
            self.assertEqual(r.status_code, 200)
