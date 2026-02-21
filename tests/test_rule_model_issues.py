"""
Unit tests for Rule model parsing from OPNsense API responses.

These tests verify that the Rule model correctly parses API responses.
Currently FAILING due to bug in Rule.sequence field definition.

Bug: Rule.py line 109 defines sequence as str with numeric constraints:
    sequence: str = Field(default="1", ge=1, le=999999, ...)

Fix: Change to int type:
    sequence: int = Field(default=1, ge=1, le=999999, ...)
"""
from unittest import TestCase
from opnsense_api.pydantic.Rule import Rule


class TestRuleModelIssues(TestCase):
    """Tests for Rule model that currently fail due to sequence field bug"""

    # Recorded API response from live OPNsense system for firewall/filter/getRule
    GET_RULE_RESPONSE = {
        "rule": {
            "enabled": "1",
            "statetype": {
                "keep": {"value": "keep state", "selected": 1},
                "sloppy": {"value": "sloppy state", "selected": 0},
                "none": {"value": "no state", "selected": 0}
            },
            "state-policy": {
                "": {"value": "default", "selected": 1},
                "if-bound": {"value": "Bind states to interface", "selected": 0}
            },
            "sequence": "100",
            "action": {
                "pass": {"value": "Pass", "selected": 1},
                "block": {"value": "Block", "selected": 0}
            },
            "quick": "1",
            "interfacenot": "0",
            "interface": {
                "lan": {"value": "LAN", "selected": 0},
                "wan": {"value": "WAN", "selected": 0}
            },
            "direction": {
                "in": {"value": "In", "selected": 1},
                "out": {"value": "Out", "selected": 0}
            },
            "ipprotocol": {
                "inet": {"value": "IPv4", "selected": 1},
                "inet6": {"value": "IPv6", "selected": 0}
            },
            "protocol": {
                "any": {"value": "any", "selected": 1}
            },
            "source_net": "any",
            "source_not": "0",
            "destination_net": "any",
            "destination_not": "0",
            "log": "0",
            "description": "Test rule"
        }
    }

    def test_rule_from_ui_dict_with_sequence(self):
        """Rule.from_ui_dict should parse API response with sequence field"""
        rule = Rule.from_ui_dict(self.GET_RULE_RESPONSE)

        self.assertTrue(rule.enabled)
        self.assertEqual(rule.action, Rule.RulesRuleActionEnum.PASS)
        self.assertEqual(rule.direction, Rule.RulesRuleDirectionEnum.IN)
        self.assertEqual(rule.description, "Test rule")

    def test_rule_instantiation_with_sequence_value(self):
        """Rule should accept sequence parameter"""
        rule = Rule(sequence=100, description="Test")

        self.assertEqual(rule.sequence, 100)
        self.assertEqual(rule.description, "Test")

    def test_rule_sequence_validates_range(self):
        """Rule.sequence should enforce ge=1, le=999999 constraints"""
        # Valid sequence
        rule = Rule(sequence=500)
        self.assertEqual(rule.sequence, 500)

        # Invalid: below minimum
        with self.assertRaises(ValueError):
            Rule(sequence=0)

        # Invalid: above maximum
        with self.assertRaises(ValueError):
            Rule(sequence=1000000)
