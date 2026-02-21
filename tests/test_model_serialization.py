import unittest
from opnsense_api.pydantic.Vlan import Vlan
from opnsense_api.pydantic.Rule import Rule
from opnsense_api.pydantic.SNATRule import Rule as SNATRule
from opnsense_api.pydantic.OneToOneRule import Rule as OneToOneRule


class TestVlanSerialization(unittest.TestCase):
    """Test Vlan model serialization with alias handling"""

    def test_interface_alias_serialization(self):
        """Test that 'interface' field serializes to 'if' alias"""
        vlan = Vlan(interface="vmx1", tag=100)
        result = vlan.to_simple_dict()

        self.assertIn('vlan', result)
        self.assertIn('if', result['vlan'])
        self.assertEqual(result['vlan']['if'], 'vmx1')
        # Should NOT have 'interface' key
        self.assertNotIn('interface', result['vlan'])

    def test_tag_serialization(self):
        """Test that tag is serialized as string"""
        vlan = Vlan(interface="vmx0", tag=200)
        result = vlan.to_simple_dict()

        self.assertEqual(result['vlan']['tag'], '200')

    def test_enum_serialization(self):
        """Test that enum fields serialize to their values"""
        vlan = Vlan(
            interface="vmx0",
            tag=100,
            pcp=Vlan.VlanVlanPcpEnum.PCP3,
            proto=Vlan.VlanVlanProtoEnum.OPT2
        )
        result = vlan.to_simple_dict()

        self.assertEqual(result['vlan']['pcp'], '3')
        self.assertEqual(result['vlan']['proto'], '802.1ad')

    def test_optional_fields_serialize_as_empty_string(self):
        """Test that None optional fields serialize as empty string"""
        vlan = Vlan(interface="vmx0", tag=100)
        result = vlan.to_simple_dict()

        self.assertEqual(result['vlan']['descr'], '')
        self.assertEqual(result['vlan']['vlanif'], '')


class TestRuleSerialization(unittest.TestCase):
    """Test firewall Rule model serialization"""

    def test_boolean_serialization(self):
        """Test that booleans serialize as '1' or '0'"""
        rule = Rule(
            enabled=True,
            quick=False,
            log=True,
            source_not=False
        )
        result = rule.to_simple_dict()

        self.assertEqual(result['rule']['enabled'], '1')
        self.assertEqual(result['rule']['quick'], '0')
        self.assertEqual(result['rule']['log'], '1')
        self.assertEqual(result['rule']['source_not'], '0')

    def test_alias_serialization(self):
        """Test that fields with aliases use the alias key"""
        # In Pydantic v2 with alias=, input must use alias keys
        rule = Rule(**{
            'state-policy': Rule.RulesRuleStatePolicyEnum.FLOATING,
            'udp-first': 30,
            'max-src-nodes': 100,
            'set-prio': Rule.RulesRuleSetPrioEnum.OPT5
        })
        result = rule.to_simple_dict()

        # Should use alias keys
        self.assertIn('state-policy', result['rule'])
        self.assertIn('udp-first', result['rule'])
        self.assertIn('max-src-nodes', result['rule'])
        self.assertIn('set-prio', result['rule'])

        # Should NOT have Python field names
        self.assertNotIn('state_policy', result['rule'])
        self.assertNotIn('udp_first', result['rule'])
        self.assertNotIn('max_src_nodes', result['rule'])
        self.assertNotIn('set_prio', result['rule'])

        # Check values
        self.assertEqual(result['rule']['state-policy'], 'floating')
        self.assertEqual(result['rule']['udp-first'], '30')
        self.assertEqual(result['rule']['max-src-nodes'], '100')
        self.assertEqual(result['rule']['set-prio'], '5')

    def test_enum_serialization(self):
        """Test that enum fields serialize to their values"""
        rule = Rule(
            action=Rule.RulesRuleActionEnum.BLOCK,
            direction=Rule.RulesRuleDirectionEnum.OUT,
            ipprotocol=Rule.RulesRuleIpprotocolEnum.INET6,
            statetype=Rule.RulesRuleStatetypeEnum.SLOPPY
        )
        result = rule.to_simple_dict()

        self.assertEqual(result['rule']['action'], 'block')
        self.assertEqual(result['rule']['direction'], 'out')
        self.assertEqual(result['rule']['ipprotocol'], 'inet6')
        self.assertEqual(result['rule']['statetype'], 'sloppy')

    def test_list_serialization(self):
        """Test that lists serialize to comma-separated strings"""
        rule = Rule(
            interface=['wan', 'lan', 'opt1'],
            source_net=['192.168.1.0/24', '10.0.0.0/8'],
            icmptype=[Rule.RulesRuleIcmptypeEnum.ECHOREQ, Rule.RulesRuleIcmptypeEnum.ECHOREP]
        )
        result = rule.to_simple_dict()

        self.assertEqual(result['rule']['interface'], 'wan,lan,opt1')
        self.assertEqual(result['rule']['source_net'], '192.168.1.0/24,10.0.0.0/8')
        self.assertEqual(result['rule']['icmptype'], 'echoreq,echorep')

    def test_integer_serialization(self):
        """Test that integers serialize as strings"""
        # Use alias keys for fields with aliases
        rule = Rule(
            sequence=500,
            statetimeout=3600,
            **{'max-src-conn': 50}
        )
        result = rule.to_simple_dict()

        self.assertEqual(result['rule']['sequence'], '500')
        self.assertEqual(result['rule']['statetimeout'], '3600')
        self.assertEqual(result['rule']['max-src-conn'], '50')

    def test_all_alias_fields(self):
        """Test all fields with aliases serialize correctly"""
        # In Pydantic v2 with alias=, input must use alias keys
        rule = Rule(**{
            'state-policy': Rule.RulesRuleStatePolicyEnum.IF_BOUND,
            'udp-first': 10,
            'udp-multiple': 20,
            'udp-single': 30,
            'max-src-nodes': 100,
            'max-src-states': 200,
            'max-src-conn': 300,
            'max-src-conn-rate': 400,
            'max-src-conn-rates': 500,
            'set-prio': Rule.RulesRuleSetPrioEnum.OPT2,
            'set-prio-low': Rule.RulesRuleSetPrioLowEnum.OPT1
        })
        result = rule.to_simple_dict()

        alias_mappings = {
            'state-policy': 'if-bound',
            'udp-first': '10',
            'udp-multiple': '20',
            'udp-single': '30',
            'max-src-nodes': '100',
            'max-src-states': '200',
            'max-src-conn': '300',
            'max-src-conn-rate': '400',
            'max-src-conn-rates': '500',
            'set-prio': '2',
            'set-prio-low': '1',
        }

        for alias, expected in alias_mappings.items():
            self.assertIn(alias, result['rule'], f"Missing alias key: {alias}")
            self.assertEqual(result['rule'][alias], expected, f"Wrong value for {alias}")


class TestSNATRuleSerialization(unittest.TestCase):
    """Test SNAT Rule model serialization"""

    def test_basic_serialization(self):
        """Test basic SNAT rule serialization"""
        rule = SNATRule(
            enabled=True,
            nonat=False,
            sequence=10,
            interface="wan",
            source_net="192.168.1.0/24",
            destination_net="any",
            target="wanip",
            log=True
        )
        result = rule.to_simple_dict()

        self.assertIn('rule', result)
        self.assertEqual(result['rule']['enabled'], '1')
        self.assertEqual(result['rule']['nonat'], '0')
        self.assertEqual(result['rule']['sequence'], '10')
        self.assertEqual(result['rule']['interface'], 'wan')
        self.assertEqual(result['rule']['source_net'], '192.168.1.0/24')
        self.assertEqual(result['rule']['target'], 'wanip')
        self.assertEqual(result['rule']['log'], '1')

    def test_enum_serialization(self):
        """Test SNAT enum serialization"""
        rule = SNATRule(
            ipprotocol=SNATRule.SnatrulesRuleIpprotocolEnum.INET6
        )
        result = rule.to_simple_dict()

        self.assertEqual(result['rule']['ipprotocol'], 'inet6')


class TestOneToOneRuleSerialization(unittest.TestCase):
    """Test 1:1 NAT Rule model serialization"""

    def test_basic_serialization(self):
        """Test basic 1:1 NAT rule serialization"""
        rule = OneToOneRule(
            enabled=True,
            log=False,
            sequence=5,
            interface="wan",
            type=OneToOneRule.TypeEnum.BINAT,
            source_net="192.168.1.100",
            external="203.0.113.50",
            natreflection=OneToOneRule.NatReflectionEnum.ENABLE
        )
        result = rule.to_simple_dict()

        self.assertIn('rule', result)
        self.assertEqual(result['rule']['enabled'], '1')
        self.assertEqual(result['rule']['log'], '0')
        self.assertEqual(result['rule']['sequence'], '5')
        self.assertEqual(result['rule']['interface'], 'wan')
        self.assertEqual(result['rule']['type'], 'binat')
        self.assertEqual(result['rule']['source_net'], '192.168.1.100')
        self.assertEqual(result['rule']['external'], '203.0.113.50')
        self.assertEqual(result['rule']['natreflection'], 'enable')

    def test_nat_type_serialization(self):
        """Test NAT type enum serialization"""
        rule = OneToOneRule(type=OneToOneRule.TypeEnum.NAT)
        result = rule.to_simple_dict()

        self.assertEqual(result['rule']['type'], 'nat')

    def test_empty_natreflection(self):
        """Test that default natreflection serializes to empty string"""
        rule = OneToOneRule(natreflection=OneToOneRule.NatReflectionEnum.DEFAULT)
        result = rule.to_simple_dict()

        self.assertEqual(result['rule']['natreflection'], '')


class TestRoundTripSerialization(unittest.TestCase):
    """Test that models can be serialized and deserialized back"""

    def test_vlan_roundtrip(self):
        """Test Vlan roundtrip serialization"""
        original = Vlan(
            interface="vmx1",
            tag=100,
            pcp=Vlan.VlanVlanPcpEnum.PCP2,
            descr="Test VLAN"
        )

        serialized = original.to_simple_dict()
        restored = Vlan.from_basic_dict(serialized)

        self.assertEqual(restored.interface, original.interface)
        self.assertEqual(restored.tag, original.tag)
        self.assertEqual(restored.pcp, original.pcp)
        self.assertEqual(restored.descr, original.descr)

    def test_rule_roundtrip(self):
        """Test Rule roundtrip serialization"""
        original = Rule(
            enabled=True,
            action=Rule.RulesRuleActionEnum.PASS,
            direction=Rule.RulesRuleDirectionEnum.IN,
            sequence=100,
            interface=['wan'],
            source_net=['any'],
            destination_net=['192.168.1.0/24'],
            destination_port='443',
            description='HTTPS inbound'
        )

        serialized = original.to_simple_dict()
        restored = Rule.from_basic_dict(serialized)

        self.assertEqual(restored.enabled, original.enabled)
        self.assertEqual(restored.action, original.action)
        self.assertEqual(restored.direction, original.direction)
        self.assertEqual(restored.sequence, original.sequence)
        self.assertEqual(restored.interface, original.interface)
        self.assertEqual(restored.destination_port, original.destination_port)
        self.assertEqual(restored.description, original.description)


if __name__ == '__main__':
    unittest.main()
