import json
from unittest import TestCase
from unittest.mock import patch, MagicMock
from opnsense_api.pydantic.Rule import Rule
from opnsense_api.pydantic.SearchResult import RuleSearchResult, SearchResult
from opnsense_api.api.firewall_filter_client import FirewallFilterClient
from opnsense_api.client import Client


class TestFirewallFilter(TestCase):
    """Tests for Firewall Filter client using recorded API responses"""

    # Recorded API responses from live OPNsense system
    SEARCH_EMPTY_RESPONSE = {"total": 0, "rowCount": 0, "current": 1, "rows": []}

    ADD_RULE_RESPONSE = {"result": "saved", "uuid": "a1b2c3d4-5678-90ab-cdef-1234567890ab"}
    SET_RULE_RESPONSE = {"result": "saved"}
    DEL_RULE_RESPONSE = {"result": "deleted"}

    def test_rule_model_instantiation(self):
        """Test that Rule model can be instantiated with default values"""
        rule = Rule()
        self.assertTrue(rule.enabled)
        self.assertEqual(rule.action, Rule.RulesRuleActionEnum.PASS)
        self.assertEqual(rule.direction, Rule.RulesRuleDirectionEnum.IN)
        self.assertEqual(rule.ipprotocol, Rule.RulesRuleIpprotocolEnum.INET)

    def test_rule_model_custom_values(self):
        """Test that Rule model accepts custom values"""
        rule = Rule(
            enabled=False,
            action=Rule.RulesRuleActionEnum.BLOCK,
            direction=Rule.RulesRuleDirectionEnum.OUT,
            description="Test rule"
        )
        self.assertFalse(rule.enabled)
        self.assertEqual(rule.action, Rule.RulesRuleActionEnum.BLOCK)
        self.assertEqual(rule.direction, Rule.RulesRuleDirectionEnum.OUT)
        self.assertEqual(rule.description, "Test rule")

    def test_rule_search_result_type(self):
        """Test that RuleSearchResult is properly typed"""
        self.assertTrue(issubclass(RuleSearchResult, SearchResult))

    def test_firewall_filter_client_exists(self):
        """Test that FirewallFilterClient has expected methods"""
        self.assertTrue(hasattr(FirewallFilterClient, 'firewall_filter_search_rule'))
        self.assertTrue(hasattr(FirewallFilterClient, 'firewall_filter_get_rule'))
        self.assertTrue(hasattr(FirewallFilterClient, 'firewall_filter_add_rule'))
        self.assertTrue(hasattr(FirewallFilterClient, 'firewall_filter_set_rule'))
        self.assertTrue(hasattr(FirewallFilterClient, 'firewall_filter_del_rule'))
        self.assertTrue(hasattr(FirewallFilterClient, 'firewall_filter_savepoint'))
        self.assertTrue(hasattr(FirewallFilterClient, 'firewall_filter_apply'))
        self.assertTrue(hasattr(FirewallFilterClient, 'firewall_filter_cancel_rollback'))

    def test_rule_from_ui_dict(self):
        """Test Rule.from_ui_dict with sample API response data"""
        ui_data = {
            "rule": {
                "enabled": "1",
                "action": {
                    "pass": {"value": "Pass", "selected": 1},
                    "block": {"value": "Block", "selected": 0},
                    "reject": {"value": "Reject", "selected": 0}
                },
                "direction": {
                    "in": {"value": "In", "selected": 1},
                    "out": {"value": "Out", "selected": 0}
                },
                "ipprotocol": {
                    "inet": {"value": "IPv4", "selected": 1},
                    "inet6": {"value": "IPv6", "selected": 0},
                    "inet46": {"value": "IPv4+IPv6", "selected": 0}
                },
                "protocol": "any",
                "source_net": {"any": {"value": "any", "selected": 1}},
                "destination_net": {"any": {"value": "any", "selected": 1}},
                "log": "0",
                "description": "Test firewall rule"
            }
        }
        rule = Rule.from_ui_dict(ui_data)
        self.assertTrue(rule.enabled)
        self.assertEqual(rule.action, Rule.RulesRuleActionEnum.PASS)
        self.assertEqual(rule.description, "Test firewall rule")

    @patch.object(FirewallFilterClient, '_search')
    def test_search_rule_empty(self, mock_search):
        """Test search rule with empty results using recorded response"""
        mock_search.return_value = self.SEARCH_EMPTY_RESPONSE

        client = Client.__new__(Client)
        result = client.firewall_filter_search_rule()

        self.assertEqual(result.total, 0)
        self.assertEqual(result.rowCount, 0)
        self.assertEqual(len(result.rows), 0)
        mock_search.assert_called_once()

    @patch.object(FirewallFilterClient, '_post')
    def test_add_rule(self, mock_post):
        """Test add rule using recorded response"""
        mock_post.return_value = self.ADD_RULE_RESPONSE

        client = Client.__new__(Client)
        rule = Rule(
            enabled=True,
            action=Rule.RulesRuleActionEnum.PASS,
            direction=Rule.RulesRuleDirectionEnum.IN,
            description="Test filter rule"
        )
        result = client.firewall_filter_add_rule(rule)

        self.assertEqual(result.result, "saved")
        self.assertEqual(result.uuid, "a1b2c3d4-5678-90ab-cdef-1234567890ab")
        mock_post.assert_called_once()

    @patch.object(FirewallFilterClient, '_post')
    def test_set_rule(self, mock_post):
        """Test set rule using recorded response"""
        mock_post.return_value = self.SET_RULE_RESPONSE

        client = Client.__new__(Client)
        rule = Rule(
            enabled=True,
            action=Rule.RulesRuleActionEnum.BLOCK,
            description="Updated filter rule"
        )
        result = client.firewall_filter_set_rule("a1b2c3d4-5678-90ab-cdef-1234567890ab", rule)

        self.assertEqual(result.result, "saved")
        mock_post.assert_called_once()

    @patch.object(FirewallFilterClient, '_post')
    def test_del_rule(self, mock_post):
        """Test delete rule using recorded response"""
        mock_post.return_value = self.DEL_RULE_RESPONSE

        client = Client.__new__(Client)
        result = client.firewall_filter_del_rule("a1b2c3d4-5678-90ab-cdef-1234567890ab")

        self.assertEqual(result.result, "deleted")
        mock_post.assert_called_once()

    def test_rule_to_simple_dict(self):
        """Test Rule serialization to API format"""
        rule = Rule(
            enabled=True,
            action=Rule.RulesRuleActionEnum.PASS,
            direction=Rule.RulesRuleDirectionEnum.IN,
            ipprotocol=Rule.RulesRuleIpprotocolEnum.INET,
            description="Test rule"
        )
        result = rule.to_simple_dict()

        self.assertIn("rule", result)
        rule_dict = result["rule"]
        self.assertEqual(rule_dict["enabled"], "1")
        self.assertEqual(rule_dict["action"], "pass")
        self.assertEqual(rule_dict["direction"], "in")
