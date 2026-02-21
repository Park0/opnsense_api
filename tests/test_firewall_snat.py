import json
from unittest import TestCase
from unittest.mock import patch, MagicMock
from opnsense_api.pydantic.SNATRule import Rule as SNATRule
from opnsense_api.pydantic.SearchResult import SNATRuleSearchResult, SearchResult
from opnsense_api.api.firewall_snat_client import FirewallSnatClient
from opnsense_api.client import Client


class TestFirewallSnat(TestCase):
    """Tests for Firewall SNAT client using recorded API responses"""

    # Recorded API responses from live OPNsense system
    SEARCH_EMPTY_RESPONSE = {"rows": [], "rowCount": 0, "total": 0, "current": 1}

    SEARCH_WITH_DATA_RESPONSE = {
        "rows": [{
            "uuid": "01bb173b-568c-4405-863f-baf6719c6ec1",
            "enabled": "1",
            "nonat": "0",
            "sequence": "1",
            "interface": "wan",
            "%interface": "WAN",
            "ipprotocol": "inet",
            "%ipprotocol": "IPv4",
            "protocol": "any",
            "source_net": "192.168.1.0/24",
            "source_not": "0",
            "source_port": "",
            "destination_net": "any",
            "destination_not": "0",
            "destination_port": "",
            "target": "wanip",
            "%target": "WAN address",
            "target_port": "",
            "log": "0",
            "categories": "",
            "tagged": "",
            "description": "Test SNAT rule from API"
        }],
        "rowCount": 1,
        "total": 1,
        "current": 1
    }

    GET_RULE_RESPONSE = {
        "rule": {
            "enabled": "1",
            "nonat": "0",
            "sequence": "1",
            "interface": {
                "lan": {"value": "LAN", "selected": 0},
                "wan": {"value": "WAN", "selected": 1}
            },
            "ipprotocol": {
                "inet": {"value": "IPv4", "selected": 1},
                "inet6": {"value": "IPv6", "selected": 0}
            },
            "protocol": {
                "any": {"value": "any", "selected": 1},
                "TCP": {"value": "TCP", "selected": 0},
                "UDP": {"value": "UDP", "selected": 0}
            },
            "source_net": "192.168.1.0/24",
            "source_not": "0",
            "source_port": "",
            "destination_net": "any",
            "destination_not": "0",
            "destination_port": "",
            "target": "wanip",
            "target_port": "",
            "log": "0",
            "categories": {},
            "tagged": "",
            "description": "Test SNAT rule from API"
        }
    }

    ADD_RULE_RESPONSE = {"result": "saved", "uuid": "01bb173b-568c-4405-863f-baf6719c6ec1"}
    SET_RULE_RESPONSE = {"result": "saved"}
    DEL_RULE_RESPONSE = {"result": "deleted"}

    def test_snat_rule_model_instantiation(self):
        """Test that SNATRule model can be instantiated with default values"""
        rule = SNATRule()
        self.assertTrue(rule.enabled)
        self.assertFalse(rule.nonat)
        self.assertEqual(rule.ipprotocol, SNATRule.SnatrulesRuleIpprotocolEnum.INET)
        self.assertEqual(rule.protocol, "any")
        self.assertEqual(rule.source_net, "any")
        self.assertEqual(rule.destination_net, "any")

    def test_snat_rule_model_custom_values(self):
        """Test that SNATRule model accepts custom values"""
        rule = SNATRule(
            enabled=False,
            nonat=True,
            interface="wan",
            ipprotocol=SNATRule.SnatrulesRuleIpprotocolEnum.INET6,
            description="Test SNAT rule"
        )
        self.assertFalse(rule.enabled)
        self.assertTrue(rule.nonat)
        self.assertEqual(rule.interface, "wan")
        self.assertEqual(rule.ipprotocol, SNATRule.SnatrulesRuleIpprotocolEnum.INET6)
        self.assertEqual(rule.description, "Test SNAT rule")

    def test_snat_rule_search_result_type(self):
        """Test that SNATRuleSearchResult is properly typed"""
        self.assertTrue(issubclass(SNATRuleSearchResult, SearchResult))

    def test_firewall_snat_client_exists(self):
        """Test that FirewallSnatClient has expected methods"""
        self.assertTrue(hasattr(FirewallSnatClient, 'firewall_snat_search_rule'))
        self.assertTrue(hasattr(FirewallSnatClient, 'firewall_snat_get_rule'))
        self.assertTrue(hasattr(FirewallSnatClient, 'firewall_snat_add_rule'))
        self.assertTrue(hasattr(FirewallSnatClient, 'firewall_snat_set_rule'))
        self.assertTrue(hasattr(FirewallSnatClient, 'firewall_snat_del_rule'))
        self.assertTrue(hasattr(FirewallSnatClient, 'firewall_snat_savepoint'))
        self.assertTrue(hasattr(FirewallSnatClient, 'firewall_snat_apply'))
        self.assertTrue(hasattr(FirewallSnatClient, 'firewall_snat_cancel_rollback'))

    def test_snat_rule_from_ui_dict(self):
        """Test SNATRule.from_ui_dict with recorded API response data"""
        rule = SNATRule.from_ui_dict(self.GET_RULE_RESPONSE)
        self.assertTrue(rule.enabled)
        self.assertFalse(rule.nonat)
        self.assertEqual(rule.interface, "wan")
        self.assertEqual(rule.ipprotocol, SNATRule.SnatrulesRuleIpprotocolEnum.INET)
        self.assertEqual(rule.source_net, "192.168.1.0/24")
        self.assertEqual(rule.description, "Test SNAT rule from API")

    @patch.object(FirewallSnatClient, '_get')
    def test_search_rule_empty(self, mock_get):
        """Test search rule with empty results using recorded response"""
        mock_get.return_value = self.SEARCH_EMPTY_RESPONSE

        client = Client.__new__(Client)
        result = client.firewall_snat_search_rule()

        self.assertEqual(result.total, 0)
        self.assertEqual(result.rowCount, 0)
        self.assertEqual(len(result.rows), 0)
        mock_get.assert_called_once()

    @patch.object(FirewallSnatClient, '_search')
    def test_search_rule_with_data(self, mock_search):
        """Test search rule with data using recorded response"""
        mock_search.return_value = self.SEARCH_WITH_DATA_RESPONSE

        client = Client.__new__(Client)
        result = client.firewall_snat_search_rule()

        self.assertEqual(result.total, 1)
        self.assertEqual(result.rowCount, 1)
        self.assertEqual(len(result.rows), 1)

        row = result.rows[0]
        self.assertTrue(row.enabled)
        self.assertEqual(row.interface, "wan")
        self.assertEqual(row.source_net, "192.168.1.0/24")
        self.assertEqual(row.description, "Test SNAT rule from API")

    @patch.object(FirewallSnatClient, '_get')
    def test_get_rule(self, mock_get):
        """Test get rule using recorded response"""
        mock_get.return_value = self.GET_RULE_RESPONSE

        client = Client.__new__(Client)
        result = client.firewall_snat_get_rule("01bb173b-568c-4405-863f-baf6719c6ec1")

        self.assertTrue(result.enabled)
        self.assertEqual(result.interface, "wan")
        self.assertEqual(result.source_net, "192.168.1.0/24")
        mock_get.assert_called_once()

    @patch.object(FirewallSnatClient, '_post')
    def test_add_rule(self, mock_post):
        """Test add rule using recorded response"""
        mock_post.return_value = self.ADD_RULE_RESPONSE

        client = Client.__new__(Client)
        rule = SNATRule(
            enabled=True,
            interface="wan",
            source_net="192.168.1.0/24",
            description="Test SNAT rule from API"
        )
        result = client.firewall_snat_add_rule(rule)

        self.assertEqual(result.result, "saved")
        self.assertEqual(result.uuid, "01bb173b-568c-4405-863f-baf6719c6ec1")
        mock_post.assert_called_once()

    @patch.object(FirewallSnatClient, '_post')
    def test_set_rule(self, mock_post):
        """Test set rule using recorded response"""
        mock_post.return_value = self.SET_RULE_RESPONSE

        client = Client.__new__(Client)
        rule = SNATRule(
            enabled=True,
            interface="wan",
            source_net="192.168.2.0/24",
            description="Updated SNAT rule"
        )
        result = client.firewall_snat_set_rule("01bb173b-568c-4405-863f-baf6719c6ec1", rule)

        self.assertEqual(result.result, "saved")
        mock_post.assert_called_once()

    @patch.object(FirewallSnatClient, '_post')
    def test_del_rule(self, mock_post):
        """Test delete rule using recorded response"""
        mock_post.return_value = self.DEL_RULE_RESPONSE

        client = Client.__new__(Client)
        result = client.firewall_snat_del_rule("01bb173b-568c-4405-863f-baf6719c6ec1")

        self.assertEqual(result.result, "deleted")
        mock_post.assert_called_once()

    def test_snat_rule_to_simple_dict(self):
        """Test SNATRule serialization to API format"""
        rule = SNATRule(
            enabled=True,
            interface="wan",
            source_net="192.168.1.0/24",
            destination_net="any",
            target="wanip",
            description="Test rule"
        )
        result = rule.to_simple_dict()

        self.assertIn("rule", result)
        rule_dict = result["rule"]
        self.assertEqual(rule_dict["enabled"], "1")
        self.assertEqual(rule_dict["interface"], "wan")
        self.assertEqual(rule_dict["source_net"], "192.168.1.0/24")
        self.assertEqual(rule_dict["nonat"], "0")
