import unittest
from opnsense_api.pydantic.Unbound import (
    Acl, Host, Alias, Dot, Blocklist,
    General, Advanced, Acls, Forwarding, UnboundSettings
)


class TestAcl(unittest.TestCase):
    """Test Acl model parsing and serialization"""

    def setUp(self):
        # Default response from API (getAcl without uuid)
        self.default_response = {
            "acl": {
                "enabled": "1",
                "name": "",
                "action": {
                    "allow": {"value": "Allow", "selected": 1},
                    "deny": {"value": "Deny", "selected": 0},
                    "refuse": {"value": "Refuse", "selected": 0},
                    "allow_snoop": {"value": "Allow Snoop", "selected": 0},
                    "deny_non_local": {"value": "Deny Non-local", "selected": 0},
                    "refuse_non_local": {"value": "Refuse Non-local", "selected": 0}
                },
                "networks": {"": {"value": "", "selected": 1}},
                "description": ""
            }
        }
        # Response from search with data
        self.search_row = {
            "uuid": "abc12345-1234-5678-9abc-def012345678",
            "enabled": "1",
            "name": "TestACL",
            "action": "allow",
            "networks": "10.0.0.0/8,192.168.0.0/16",
            "description": "Test Access List"
        }

    def test_parse_defaults(self):
        """Test parsing default ACL response"""
        acl = Acl.from_ui_dict(self.default_response)
        self.assertTrue(acl.enabled)
        self.assertIsNone(acl.name)
        self.assertEqual(acl.action, Acl.AclsAclActionEnum.ALLOW)
        self.assertEqual(acl.networks, [])
        self.assertIsNone(acl.description)

    def test_parse_search_row(self):
        """Test parsing ACL from search result"""
        acl = Acl.from_ui_dict(self.search_row)
        self.assertEqual(acl.name, "TestACL")
        self.assertEqual(acl.action, Acl.AclsAclActionEnum.ALLOW)
        self.assertEqual(acl.description, "Test Access List")
        self.assertEqual(str(acl.uuid), "abc12345-1234-5678-9abc-def012345678")

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        acl = Acl(
            enabled=True,
            name="MyACL",
            action=Acl.AclsAclActionEnum.DENY,
            networks=["10.0.0.0/8"],
            description="My Access List"
        )
        data = acl.to_simple_dict()
        self.assertIn("acl", data)
        self.assertEqual(data["acl"]["name"], "MyACL")
        self.assertEqual(data["acl"]["action"], "deny")
        self.assertEqual(data["acl"]["description"], "My Access List")
        self.assertEqual(data["acl"]["enabled"], "1")

    def test_action_enum_values(self):
        """Test action enum has correct values"""
        self.assertEqual(Acl.AclsAclActionEnum.ALLOW.value, "allow")
        self.assertEqual(Acl.AclsAclActionEnum.DENY.value, "deny")
        self.assertEqual(Acl.AclsAclActionEnum.REFUSE.value, "refuse")
        self.assertEqual(Acl.AclsAclActionEnum.ALLOW_SNOOP.value, "allow_snoop")


class TestHost(unittest.TestCase):
    """Test Host (host override) model parsing and serialization"""

    def setUp(self):
        # Default response from API
        self.default_response = {
            "host": {
                "enabled": "1",
                "hostname": "",
                "domain": "",
                "rr": {
                    "A": {"value": "A (IPv4 address)", "selected": 1},
                    "AAAA": {"value": "AAAA (IPv6 address)", "selected": 0},
                    "MX": {"value": "MX (mail server)", "selected": 0},
                    "TXT": {"value": "TXT (text)", "selected": 0}
                },
                "mxprio": "",
                "mx": "",
                "ttl": "",
                "server": "",
                "txtdata": "",
                "aliascount": "",
                "description": ""
            }
        }
        # Response from search with data
        self.search_row = {
            "uuid": "964f18f1-f09b-44df-8341-79ea23090260",
            "enabled": "1",
            "hostname": "openbao",
            "domain": "example.lan",
            "rr": "A",
            "%rr": "A (IPv4 address)",
            "mxprio": "",
            "mx": "",
            "ttl": "",
            "server": "10.0.19.253",
            "txtdata": "",
            "aliascount": "0",
            "description": ""
        }

    def test_parse_defaults(self):
        """Test parsing default host response"""
        host = Host.from_ui_dict(self.default_response)
        self.assertTrue(host.enabled)
        self.assertIsNone(host.hostname)
        self.assertIsNone(host.domain)
        self.assertEqual(host.rr, Host.HostsHostRrEnum.A)
        self.assertIsNone(host.server)

    def test_parse_search_row(self):
        """Test parsing host from search result"""
        host = Host.from_ui_dict(self.search_row)
        self.assertEqual(host.hostname, "openbao")
        self.assertEqual(host.domain, "example.lan")
        self.assertEqual(host.server, "10.0.19.253")
        self.assertEqual(host.rr, Host.HostsHostRrEnum.A)
        self.assertEqual(str(host.uuid), "964f18f1-f09b-44df-8341-79ea23090260")

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        host = Host(
            enabled=True,
            hostname="testhost",
            domain="example.lan",
            server="192.168.1.100",
            description="Test host override"
        )
        data = host.to_simple_dict()
        self.assertIn("host", data)
        self.assertEqual(data["host"]["hostname"], "testhost")
        self.assertEqual(data["host"]["domain"], "example.lan")
        self.assertEqual(data["host"]["server"], "192.168.1.100")
        self.assertEqual(data["host"]["rr"], "A")
        self.assertEqual(data["host"]["enabled"], "1")

    def test_rr_enum_values(self):
        """Test RR enum has correct values"""
        self.assertEqual(Host.HostsHostRrEnum.A.value, "A")
        self.assertEqual(Host.HostsHostRrEnum.AAAA.value, "AAAA")
        self.assertEqual(Host.HostsHostRrEnum.MX.value, "MX")
        self.assertEqual(Host.HostsHostRrEnum.TXT.value, "TXT")


class TestDot(unittest.TestCase):
    """Test Dot (forward/DoT) model parsing and serialization"""

    def setUp(self):
        # Default response from API
        self.default_response = {
            "dot": {
                "enabled": "1",
                "type": {
                    "dot": {"value": "DNS over TLS", "selected": 1},
                    "forward": {"value": "Forward", "selected": 0}
                },
                "domain": "",
                "server": "",
                "port": "",
                "verify": "",
                "forward_tcp_upstream": "0",
                "forward_first": "0",
                "description": ""
            }
        }
        # Data for forward entry
        self.forward_data = {
            "uuid": "12345678-1234-5678-9abc-def012345678",
            "enabled": "1",
            "type": "dot",
            "domain": "",
            "server": "1.1.1.1",
            "port": "853",
            "verify": "cloudflare-dns.com",
            "forward_tcp_upstream": "0",
            "forward_first": "0",
            "description": "Cloudflare DoT"
        }

    def test_parse_defaults(self):
        """Test parsing default forward response"""
        dot = Dot.from_ui_dict(self.default_response)
        self.assertTrue(dot.enabled)
        self.assertEqual(dot.type, Dot.DotsDotTypeEnum.DOT)
        self.assertIsNone(dot.server)
        self.assertFalse(dot.forward_tcp_upstream)
        self.assertFalse(dot.forward_first)

    def test_parse_forward_data(self):
        """Test parsing forward entry"""
        dot = Dot.from_ui_dict(self.forward_data)
        self.assertEqual(dot.server, "1.1.1.1")
        self.assertEqual(dot.port, 853)
        self.assertEqual(dot.verify, "cloudflare-dns.com")
        self.assertEqual(dot.description, "Cloudflare DoT")

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        dot = Dot(
            enabled=True,
            type=Dot.DotsDotTypeEnum.DOT,
            server="8.8.8.8",
            port=853,
            verify="dns.google",
            description="Google DoT"
        )
        data = dot.to_simple_dict()
        self.assertIn("dot", data)
        self.assertEqual(data["dot"]["server"], "8.8.8.8")
        self.assertEqual(data["dot"]["port"], "853")
        self.assertEqual(data["dot"]["type"], "dot")
        self.assertEqual(data["dot"]["enabled"], "1")

    def test_type_enum_values(self):
        """Test type enum has correct values"""
        self.assertEqual(Dot.DotsDotTypeEnum.DOT.value, "dot")
        self.assertEqual(Dot.DotsDotTypeEnum.FORWARD.value, "forward")


class TestAlias(unittest.TestCase):
    """Test Alias (host alias) model parsing and serialization"""

    def setUp(self):
        self.default_response = {
            "alias": {
                "enabled": "1",
                "host": {"": {"value": "", "selected": 1}},
                "hostname": "",
                "domain": "",
                "description": ""
            }
        }
        self.alias_data = {
            "uuid": "abcd1234-1234-5678-9abc-def012345678",
            "enabled": "1",
            "host": "964f18f1-f09b-44df-8341-79ea23090260",
            "hostname": "alias1",
            "domain": "example.lan",
            "description": "Test alias"
        }

    def test_parse_defaults(self):
        """Test parsing default alias response"""
        alias = Alias.from_ui_dict(self.default_response)
        self.assertTrue(alias.enabled)
        self.assertIsNone(alias.host)
        self.assertIsNone(alias.hostname)

    def test_parse_alias_data(self):
        """Test parsing alias data"""
        alias = Alias.from_ui_dict(self.alias_data)
        self.assertEqual(alias.host, "964f18f1-f09b-44df-8341-79ea23090260")
        self.assertEqual(alias.hostname, "alias1")
        self.assertEqual(alias.domain, "example.lan")

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        alias = Alias(
            enabled=True,
            host="some-uuid",
            hostname="myalias",
            domain="test.lan",
            description="My Alias"
        )
        data = alias.to_simple_dict()
        self.assertIn("alias", data)
        self.assertEqual(data["alias"]["host"], "some-uuid")
        self.assertEqual(data["alias"]["hostname"], "myalias")
        self.assertEqual(data["alias"]["enabled"], "1")


class TestBlocklist(unittest.TestCase):
    """Test Blocklist (DNSBL) model parsing and serialization"""

    def setUp(self):
        self.default_response = {
            "blocklist": {
                "enabled": "1",
                "type": {"ag": {"value": "AdGuard List", "selected": 0}},
                "lists": {"": {"value": "", "selected": 1}},
                "allowlists": {"": {"value": "", "selected": 1}},
                "blocklists": {"": {"value": "", "selected": 1}},
                "wildcards": {"": {"value": "", "selected": 1}},
                "source_nets": {"": {"value": "", "selected": 1}},
                "address": "",
                "nxdomain": "",
                "cache_ttl": "72000",
                "description": ""
            }
        }

    def test_parse_defaults(self):
        """Test parsing default blocklist response"""
        bl = Blocklist.from_ui_dict(self.default_response)
        self.assertTrue(bl.enabled)
        self.assertEqual(bl.cache_ttl, 72000)
        self.assertEqual(bl.type, [])

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        bl = Blocklist(
            enabled=True,
            type=[Blocklist.DnsblBlocklistTypeEnum.AG],
            description="AdGuard blocking",
            cache_ttl=36000
        )
        data = bl.to_simple_dict()
        self.assertIn("blocklist", data)
        self.assertEqual(data["blocklist"]["enabled"], "1")
        self.assertEqual(data["blocklist"]["cache_ttl"], "36000")


class TestGeneral(unittest.TestCase):
    """Test General settings model parsing and serialization"""

    def test_create_general(self):
        """Test creating General settings"""
        general = General(
            enabled=True,
            port=53,
            dnssec=True,
            local_zone_type=General.GeneralGeneralLocalZoneTypeEnum.TRANSPARENT
        )
        self.assertTrue(general.enabled)
        self.assertEqual(general.port, 53)
        self.assertTrue(general.dnssec)

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        general = General(
            enabled=True,
            port=53
        )
        data = general.to_simple_dict()
        self.assertIn("general", data)
        self.assertEqual(data["general"]["enabled"], "1")
        self.assertEqual(data["general"]["port"], "53")

    def test_local_zone_type_enum(self):
        """Test local zone type enum values"""
        self.assertEqual(General.GeneralGeneralLocalZoneTypeEnum.TRANSPARENT.value, "transparent")
        self.assertEqual(General.GeneralGeneralLocalZoneTypeEnum.DENY.value, "deny")
        self.assertEqual(General.GeneralGeneralLocalZoneTypeEnum.REFUSE.value, "refuse")


class TestAdvanced(unittest.TestCase):
    """Test Advanced settings model"""

    def test_create_advanced(self):
        """Test creating Advanced settings"""
        advanced = Advanced(
            hideidentity=True,
            hideversion=True,
            prefetch=True,
            aggressivensec=True,
            logverbosity=Advanced.AdvancedAdvancedLogverbosityEnum.X1
        )
        self.assertTrue(advanced.hideidentity)
        self.assertTrue(advanced.hideversion)
        self.assertTrue(advanced.prefetch)
        self.assertTrue(advanced.aggressivensec)

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        advanced = Advanced(
            hideidentity=True,
            aggressivensec=True
        )
        data = advanced.to_simple_dict()
        self.assertIn("advanced", data)
        self.assertEqual(data["advanced"]["hideidentity"], "1")
        self.assertEqual(data["advanced"]["aggressivensec"], "1")


class TestAcls(unittest.TestCase):
    """Test Acls section settings model"""

    def test_default_action_enum(self):
        """Test default action enum values"""
        self.assertEqual(Acls.AclsAclsDefaultActionEnum.ALLOW.value, "allow")
        self.assertEqual(Acls.AclsAclsDefaultActionEnum.DENY.value, "deny")
        self.assertEqual(Acls.AclsAclsDefaultActionEnum.REFUSE.value, "refuse")

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        acls = Acls(
            default_action=Acls.AclsAclsDefaultActionEnum.DENY
        )
        data = acls.to_simple_dict()
        self.assertIn("acls", data)
        self.assertEqual(data["acls"]["default_action"], "deny")


class TestForwarding(unittest.TestCase):
    """Test Forwarding settings model"""

    def test_create_forwarding(self):
        """Test creating Forwarding settings"""
        forwarding = Forwarding(enabled=True)
        self.assertTrue(forwarding.enabled)

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        forwarding = Forwarding(enabled=True)
        data = forwarding.to_simple_dict()
        self.assertIn("forwarding", data)
        self.assertEqual(data["forwarding"]["enabled"], "1")


class TestUnboundSettings(unittest.TestCase):
    """Test UnboundSettings wrapper model"""

    def setUp(self):
        # Sample API response (simplified)
        self.api_response = {
            "unbound": {
                "general": {
                    "enabled": "1",
                    "port": "53",
                    "dnssec": "",
                    "local_zone_type": {
                        "transparent": {"value": "transparent", "selected": 1},
                        "deny": {"value": "deny", "selected": 0}
                    }
                },
                "advanced": {
                    "hideidentity": "",
                    "aggressivensec": "1",
                    "logverbosity": {
                        "0": {"value": "Level 0", "selected": 0},
                        "1": {"value": "Level 1 (Default)", "selected": 1}
                    },
                    "valloglevel": {
                        "0": {"value": "Level 0 (Default)", "selected": 1},
                        "1": {"value": "Level 1", "selected": 0}
                    }
                },
                "acls": {
                    "default_action": {
                        "allow": {"value": "Allow", "selected": 1},
                        "deny": {"value": "Deny", "selected": 0}
                    }
                },
                "forwarding": {
                    "enabled": ""
                }
            }
        }

    def test_parse_api_response(self):
        """Test parsing full API response"""
        settings = UnboundSettings.from_ui_dict(self.api_response)
        self.assertIsNotNone(settings.general)
        self.assertIsNotNone(settings.advanced)
        self.assertIsNotNone(settings.acls)
        self.assertIsNotNone(settings.forwarding)
        self.assertTrue(settings.general.enabled)
        self.assertEqual(settings.general.port, 53)
        self.assertTrue(settings.advanced.aggressivensec)

    def test_serialize_to_api_format(self):
        """Test serialization to API format"""
        settings = UnboundSettings(
            general=General(enabled=True, port=53),
            forwarding=Forwarding(enabled=True)
        )
        data = settings.to_simple_dict()
        self.assertIn("unbound", data)
        self.assertIn("general", data["unbound"])
        self.assertIn("forwarding", data["unbound"])
        self.assertEqual(data["unbound"]["general"]["enabled"], "1")
        self.assertEqual(data["unbound"]["forwarding"]["enabled"], "1")

    def test_partial_settings(self):
        """Test creating partial settings (only general)"""
        settings = UnboundSettings(
            general=General(enabled=False)
        )
        data = settings.to_simple_dict()
        self.assertIn("unbound", data)
        self.assertIn("general", data["unbound"])
        self.assertNotIn("advanced", data["unbound"])
        self.assertEqual(data["unbound"]["general"]["enabled"], "0")


if __name__ == '__main__':
    unittest.main()
