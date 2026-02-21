import json
from unittest import TestCase
from opnsense_api.api.helper import Helper
from opnsense_api.pydantic.Frontend import Frontend
from opnsense_api.pydantic.Result import Result


class TestHelper(TestCase):

    def test_config_test(self):
        self.assertFalse(Helper.config_has_errors(Result(**json.loads("{\"result\": \"\\n\\n\"}"))))