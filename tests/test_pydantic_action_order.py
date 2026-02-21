import json
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import UUID

from opnsense_api.client import Client
from opnsense_api.pydantic.Action import Action
from opnsense_api.pydantic.Frontend import Frontend
from opnsense_api.pydantic.SearchResult import ActionSearchResult


class TestPydanticActionOrder(TestCase):

    def setUp(self):
        self.checker = Client(None,None,None, None)
        self.frontend = Frontend(
            linkedActions=["00000000-0000-0000-0000-000000000004",
                           "00000000-0000-0000-0000-000000000001",
                           "00000000-0000-0000-0000-000000000003",
                           "00000000-0000-0000-0000-000000000005",
                           "00000000-0000-0000-0000-000000000002",
                           "00000000-0000-0000-0000-000000000006",
                           "00000000-0000-0000-0000-000000000007",
                           "00000000-0000-0000-0000-000000000008"],
            name='Test',
            bind=['0.0.0.0']
        )

        # Mock actions
        self.actions = ActionSearchResult(rowCount=5, total=5, current=1, rows=[
            Action(uuid=UUID("00000000-0000-0000-0000-000000000001"), name="action_app_dot_sso_dot_lan", # 8
                   type=Action.ActionsActionTypeEnum.USE_BACKEND),
            Action(uuid=UUID("00000000-0000-0000-0000-000000000002"), name="action_app_dot_sso_dot_lan_auth", # 1
                   type=Action.ActionsActionTypeEnum.USE_BACKEND),
            Action(uuid=UUID("00000000-0000-0000-0000-000000000003"), name="redirect", # 6
                   type=Action.ActionsActionTypeEnum.USE_BACKEND),
            Action(uuid=UUID("00000000-0000-0000-0000-000000000004"), name="auth-deny", # 7
                   type=Action.ActionsActionTypeEnum.USE_BACKEND),
            Action(uuid=UUID("00000000-0000-0000-0000-000000000005"), name="X-Forward-Proto", # 4
                   type=Action.ActionsActionTypeEnum.USE_BACKEND),
            Action(uuid=UUID("00000000-0000-0000-0000-000000000006"), name="schema-http", # 2
                   type=Action.ActionsActionTypeEnum.USE_BACKEND),
            Action(uuid=UUID("00000000-0000-0000-0000-000000000007"), name="schema-https", # 3
                   type=Action.ActionsActionTypeEnum.USE_BACKEND),
            Action(uuid=UUID("00000000-0000-0000-0000-000000000008"), name="lua-auth-intercept", # 5
                   type=Action.ActionsActionTypeEnum.USE_BACKEND),
        ])
        self.checker.haproxy_settings_searchActions = MagicMock(return_value=self.actions)

    def test_acl_ordering(self):
        self.checker.haproxy_check_acl_order(self.frontend)

        # Expected order according to rules:
        # - action_*_auth first, ordered by AUTH_SUBORDER
        # - other action_* after
        # - non-action_* last
        expected_order = [
                            '00000000-0000-0000-0000-000000000002',
                            '00000000-0000-0000-0000-000000000006',
                            '00000000-0000-0000-0000-000000000007',
                            '00000000-0000-0000-0000-000000000005',
                            '00000000-0000-0000-0000-000000000008',
                            '00000000-0000-0000-0000-000000000003',
                            '00000000-0000-0000-0000-000000000004',
                            '00000000-0000-0000-0000-000000000001'
                          ]

        self.assertEqual(self.frontend.linkedActions, expected_order)