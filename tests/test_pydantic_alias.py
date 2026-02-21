import json
from unittest import TestCase
from opnsense_api.pydantic.Alias import Alias


class TestPydanticAlias(TestCase):

    def data_alias_1(self):
        return """
{"alias":{"enabled":"1","name":"bogons","type":{"host":{"value":"Host(s)","selected":0},"network":{"value":"Network(s)","selected":0},"port":{"value":"Port(s)","selected":0},"url":{"value":"URL (IPs)","selected":0},"urltable":{"value":"URL Table (IPs)","selected":0},"urljson":{"value":"URL Table in JSON format (IPs)","selected":0},"geoip":{"value":"GeoIP","selected":0},"networkgroup":{"value":"Network group","selected":0},"mac":{"value":"MAC address","selected":0},"asn":{"value":"BGP ASN","selected":0},"dynipv6host":{"value":"Dynamic IPv6 Host","selected":0},"authgroup":{"value":"OpenVPN group","selected":0},"internal":{"value":"Internal (automatic)","selected":0},"external":{"value":"External (advanced)","selected":1}},"path_expression":"","proto":{"IPv4":{"value":"IPv4","selected":0},"IPv6":{"value":"IPv6","selected":0}},"interface":{"":{"value":"None","selected":1},"lan":{"value":"LAN","selected":0},"wan":{"value":"WAN","selected":0}},"counters":"","updatefreq":"","content":{"":{"value":"","selected":1},"test":{"selected":0,"value":"test","description":""},"__wan_network":{"selected":0,"value":"__wan_network","description":"wan net"},"__lan_network":{"selected":0,"value":"__lan_network","description":"lan net"},"__lo0_network":{"selected":0,"value":"__lo0_network","description":"Loopback net"},"bogons":{"selected":0,"value":"bogons","description":"bogon networks (internal)"},"bogonsv6":{"selected":0,"value":"bogonsv6","description":"bogon networks IPv6 (internal)"},"virusprot":{"selected":0,"value":"virusprot","description":"overload table for rate limiting (internal)"},"sshlockout":{"selected":0,"value":"sshlockout","description":"abuse lockout table (internal)"}},"password":"","username":"","authtype":{"":{"value":"None","selected":1},"Basic":{"value":"Basic","selected":0},"Bearer":{"value":"Bearer","selected":0},"Header":{"value":"Header","selected":0}},"expire":"","categories":[],"current_items":"2868","last_updated":"","eval_nomatch":"0","eval_match":"0","in_block_p":"0","in_block_b":"0","in_pass_p":"0","in_pass_b":"0","out_block_p":"0","out_block_b":"0","out_pass_p":"0","out_pass_b":"0","description":"bogon networks (internal)"}}
"""

    def test_alias_load(self):
        alias_str = self.data_alias_1()
        alias_json = json.loads(alias_str)
        alias = Alias.from_ui_dict(alias_json)
        self.assertEqual('bogons', alias.name)

    def test_alias_search_row(self):
        """Test parsing alias from search result row"""
        row = {
            'uuid': 'bogons',
            'enabled': '1',
            'name': 'bogons',
            'type': 'external',
            'current_items': 2884,
            'eval_nomatch': 711,
            'eval_match': 5,
            'in_block_p': 5,
            'in_block_b': 180,
            'in_pass_p': 0,
            'in_pass_b': 0,
            'out_block_p': 0,
            'out_block_b': 0,
            'out_pass_p': 0,
            'out_pass_b': 0,
            'description': 'bogon networks (internal)'
        }
        alias = Alias.from_ui_dict(row)
        self.assertEqual('bogons', alias.name)
        self.assertEqual('bogons', alias.uuid)
        self.assertTrue(alias.enabled)
        self.assertEqual(Alias.AliasesAliasTypeEnum.EXTERNAL, alias.type)
        self.assertEqual(2884, alias.current_items)
        self.assertEqual(711, alias.eval_nomatch)
        self.assertEqual(5, alias.eval_match)
        self.assertEqual(5, alias.in_block_p)
        self.assertEqual(180, alias.in_block_b)
        self.assertEqual(0, alias.in_pass_p)
        self.assertEqual(0, alias.in_pass_b)
        self.assertEqual(0, alias.out_block_p)
        self.assertEqual(0, alias.out_block_b)
        self.assertEqual(0, alias.out_pass_p)
        self.assertEqual(0, alias.out_pass_b)
        self.assertEqual('bogon networks (internal)', alias.description)
