import json
from unittest import TestCase
from unittest.mock import MagicMock, patch

from opnsense_api.client import Client
from opnsense_api.pydantic.Acl import Acl


class TestPydanticAuth(TestCase):

    def data_user_api_search_full_1(self):
        return """
{
  "total": 2,
  "rowCount": 2,
  "current": 1,
  "rows": [
    {
      "username": "root",
      "key": "ergojeasrtghjksdrtgjserjejFewfjoNMEWFGPOIJGoieJNGMNJMWGONMWSERGNSOEGNSEGNOSEGNOO",
      "id": "greargaerkgbvpaerkgvesprgkbHHKORLFKLKGHhEaergaergazegaegdrogmhbdorghmRHBRKHNgkedrgredgrgdrgdrgbrdg"
    },
    {
      "username": "api",
      "key": "erghaerghplaergGw4jgoH$EGmTEgfMGMGMGMgMGMGMMGmsegmsorgesomegfNEogZEMEOMomgMOEgmos",
      "id": "greargaerkgbvpaerkgvesprgkbHHKORLFKLKwergwesrgvedsrgvbdrgbaedrtghsaeHBRKHNgkedrgredgrgdrgdrgbrdg="
    }
  ]
}
"""

    def data_user_api_search_full_2(self):
        return """
{
  "rows": [
    {
      "uuid": "f3c2b9d8-6f47-4c6e-9a0a-1c8a7c1e5d2b",
      "uid": "0",
      "name": "root",
      "disabled": "0",
      "scope": "system",
      "expires": "",
      "authorizedkeys": "",
      "%authorizedkeys": "",
      "otp_seed": "",
      "shell": "",
      "password": "",
      "%password": "",
      "scrambled_password": "0",
      "pwd_changed_at": "",
      "landing_page": "",
      "comment": "",
      "email": "admin@localhost.lan",
      "apikeys": "",
      "%apikeys": "",
      "priv": "",
      "language": "",
      "group_memberships": "1999",
      "%group_memberships": "admins",
      "descr": "System Administrator",
      "dashboard": "",
      "is_admin": "1",
      "shell_warning": "0"
    }
  ],
  "rowCount": 1,
  "total": 1,
  "current": 1
}
        """

    @patch("requests.get")
    def test_load_cert_search_1(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = self.data_user_api_search_full_1()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}

        mock_get.return_value = mock_resp


        self.checker = Client(None, None, None, None)
        search_result = self.checker.auth_user_search_api_key()
        self.assertEqual(search_result.rowCount, 2)
        self.assertEqual(search_result.rows[0].username, "root")
        self.assertEqual(search_result.rows[1].username, "api")

    @patch("requests.get")
    def test_load_cert_search_2(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = self.data_user_api_search_full_2()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}

        mock_get.return_value = mock_resp


        self.checker = Client(None, None, None, None)
        search_result = self.checker.auth_user_search()
        self.assertEqual(search_result.rowCount, 1)
        self.assertEqual(str(search_result.rows[0].uuid), "f3c2b9d8-6f47-4c6e-9a0a-1c8a7c1e5d2b")
