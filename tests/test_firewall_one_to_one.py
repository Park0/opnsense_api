from unittest import TestCase
from unittest.mock import patch
from opnsense_api.pydantic.OneToOneRule import Rule as OneToOneRule
from opnsense_api.pydantic.SearchResult import OneToOneRuleSearchResult, SearchResult
from opnsense_api.api.firewall_one_to_one_client import FirewallOneToOneClient
from opnsense_api.client import Client


class TestFirewallOneToOne(TestCase):
    """Tests for Firewall 1:1 NAT client using recorded API responses"""

    SEARCH_EMPTY_RESPONSE = {"rows": [], "rowCount": 0, "total": 0, "current": 1}

    SEARCH_WITH_DATA_RESPONSE = {
        "rows": [{
            "uuid": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
            "enabled": "1",
            "log": "0",
            "sequence": "1",
            "interface": "wan",
            "type": "binat",
            "source_net": "192.168.1.100",
            "source_not": "0",
            "destination_net": "any",
            "destination_not": "0",
            "external": "203.0.113.50",
            "natreflection": "",
            "categories": "",
            "description": "Web server NAT"
        }],
        "rowCount": 1,
        "total": 1,
        "current": 1
    }

    GET_RULE_RESPONSE = {
        "rule": {
            "enabled": "1",
            "log": "0",
            "sequence": "1",
            "interface": {
                "lan": {"value": "LAN", "selected": 0},
                "wan": {"value": "WAN", "selected": 1}
            },
            "type": {
                "binat": {"value": "BINAT", "selected": 1},
                "nat": {"value": "NAT", "selected": 0}
            },
            "source_net": "192.168.1.100",
            "source_not": "0",
            "destination_net": "any",
            "destination_not": "0",
            "external": "203.0.113.50",
            "natreflection": {
                "": {"value": "Default", "selected": 1},
                "enable": {"value": "Enable", "selected": 0},
                "disable": {"value": "Disable", "selected": 0}
            },
            "categories": {},
            "description": "Web server NAT"
        }
    }

    ADD_RULE_RESPONSE = {"result": "saved", "uuid": "a1b2c3d4-5678-90ab-cdef-1234567890ab"}
    SET_RULE_RESPONSE = {"result": "saved"}
    DEL_RULE_RESPONSE = {"result": "deleted"}

    def test_one_to_one_rule_model_instantiation(self):
        """Test that OneToOneRule model can be instantiated with default values"""
        rule = OneToOneRule()
        self.assertTrue(rule.enabled)
        self.assertFalse(rule.log)
        self.assertEqual(rule.type, OneToOneRule.TypeEnum.BINAT)
        self.assertEqual(rule.interface, "wan")
        self.assertEqual(rule.natreflection, OneToOneRule.NatReflectionEnum.DEFAULT)

    def test_one_to_one_rule_model_custom_values(self):
        """Test that OneToOneRule model accepts custom values"""
        rule = OneToOneRule(
            enabled=True,
            interface="wan",
            type=OneToOneRule.TypeEnum.NAT,
            source_net="192.168.1.100",
            external="203.0.113.50",
            natreflection=OneToOneRule.NatReflectionEnum.ENABLE,
            description="Test 1:1 NAT"
        )
        self.assertTrue(rule.enabled)
        self.assertEqual(rule.type, OneToOneRule.TypeEnum.NAT)
        self.assertEqual(rule.source_net, "192.168.1.100")
        self.assertEqual(rule.external, "203.0.113.50")
        self.assertEqual(rule.natreflection, OneToOneRule.NatReflectionEnum.ENABLE)

    def test_one_to_one_rule_search_result_type(self):
        """Test that OneToOneRuleSearchResult is properly typed"""
        self.assertTrue(issubclass(OneToOneRuleSearchResult, SearchResult))

    def test_firewall_one_to_one_client_methods_exist(self):
        """Test that FirewallOneToOneClient has all expected methods"""
        self.assertTrue(hasattr(FirewallOneToOneClient, 'firewall_one_to_one_search_rule'))
        self.assertTrue(hasattr(FirewallOneToOneClient, 'firewall_one_to_one_get_rule'))
        self.assertTrue(hasattr(FirewallOneToOneClient, 'firewall_one_to_one_add_rule'))
        self.assertTrue(hasattr(FirewallOneToOneClient, 'firewall_one_to_one_set_rule'))
        self.assertTrue(hasattr(FirewallOneToOneClient, 'firewall_one_to_one_del_rule'))
        self.assertTrue(hasattr(FirewallOneToOneClient, 'firewall_one_to_one_savepoint'))
        self.assertTrue(hasattr(FirewallOneToOneClient, 'firewall_one_to_one_apply'))
        self.assertTrue(hasattr(FirewallOneToOneClient, 'firewall_one_to_one_cancel_rollback'))

    def test_one_to_one_rule_from_ui_dict(self):
        """Test OneToOneRule.from_ui_dict with recorded API response"""
        rule = OneToOneRule.from_ui_dict(self.GET_RULE_RESPONSE)
        self.assertTrue(rule.enabled)
        self.assertEqual(rule.interface, "wan")
        self.assertEqual(rule.type, OneToOneRule.TypeEnum.BINAT)
        self.assertEqual(rule.source_net, "192.168.1.100")
        self.assertEqual(rule.external, "203.0.113.50")
        self.assertEqual(rule.description, "Web server NAT")

    @patch.object(FirewallOneToOneClient, '_search')
    def test_search_rule_empty(self, mock_search):
        """Test search rule with empty results"""
        mock_search.return_value = self.SEARCH_EMPTY_RESPONSE
        client = Client.__new__(Client)
        result = client.firewall_one_to_one_search_rule()
        self.assertEqual(result.total, 0)
        self.assertEqual(len(result.rows), 0)

    @patch.object(FirewallOneToOneClient, '_search')
    def test_search_rule_with_data(self, mock_search):
        """Test search rule with data"""
        mock_search.return_value = self.SEARCH_WITH_DATA_RESPONSE
        client = Client.__new__(Client)
        result = client.firewall_one_to_one_search_rule()
        self.assertEqual(result.total, 1)
        self.assertEqual(result.rows[0].source_net, "192.168.1.100")
        self.assertEqual(result.rows[0].external, "203.0.113.50")

    @patch.object(FirewallOneToOneClient, '_get')
    def test_get_rule(self, mock_get):
        """Test get rule"""
        mock_get.return_value = self.GET_RULE_RESPONSE
        client = Client.__new__(Client)
        result = client.firewall_one_to_one_get_rule("a1b2c3d4-5678-90ab-cdef-1234567890ab")
        self.assertTrue(result.enabled)
        self.assertEqual(result.external, "203.0.113.50")

    @patch.object(FirewallOneToOneClient, '_post')
    def test_add_rule(self, mock_post):
        """Test add rule"""
        mock_post.return_value = self.ADD_RULE_RESPONSE
        client = Client.__new__(Client)
        rule = OneToOneRule(source_net="192.168.1.100", external="203.0.113.50")
        result = client.firewall_one_to_one_add_rule(rule)
        self.assertEqual(result.result, "saved")
        self.assertIsNotNone(result.uuid)

    @patch.object(FirewallOneToOneClient, '_post')
    def test_set_rule(self, mock_post):
        """Test set rule"""
        mock_post.return_value = self.SET_RULE_RESPONSE
        client = Client.__new__(Client)
        rule = OneToOneRule(source_net="192.168.1.101", external="203.0.113.51")
        result = client.firewall_one_to_one_set_rule("a1b2c3d4-5678-90ab-cdef-1234567890ab", rule)
        self.assertEqual(result.result, "saved")

    @patch.object(FirewallOneToOneClient, '_post')
    def test_del_rule(self, mock_post):
        """Test delete rule"""
        mock_post.return_value = self.DEL_RULE_RESPONSE
        client = Client.__new__(Client)
        result = client.firewall_one_to_one_del_rule("a1b2c3d4-5678-90ab-cdef-1234567890ab")
        self.assertEqual(result.result, "deleted")

    def test_one_to_one_rule_to_simple_dict(self):
        """Test OneToOneRule serialization to API format"""
        rule = OneToOneRule(
            enabled=True,
            interface="wan",
            type=OneToOneRule.TypeEnum.BINAT,
            source_net="192.168.1.100",
            external="203.0.113.50",
            description="Test rule"
        )
        result = rule.to_simple_dict()
        self.assertIn("rule", result)
        rule_dict = result["rule"]
        self.assertEqual(rule_dict["enabled"], "1")
        self.assertEqual(rule_dict["interface"], "wan")
        self.assertEqual(rule_dict["type"], "binat")
        self.assertEqual(rule_dict["source_net"], "192.168.1.100")
        self.assertEqual(rule_dict["external"], "203.0.113.50")
