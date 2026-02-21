"""
Tests for the desired state configuration system.
"""
import unittest
from unittest.mock import Mock, MagicMock
from uuid import UUID

from opnsense_api.state import StateManager, StateChange, ChangeType
from opnsense_api.state.handlers import (
    EntityHandler, DnsHostHandler, DhcpReservationHandler, FirewallAliasHandler
)
from opnsense_api.pydantic.Unbound import Host
from opnsense_api.pydantic.KeaDhcpv4 import Reservation
from opnsense_api.pydantic.Alias import Alias


class TestStateChange(unittest.TestCase):
    """Test StateChange dataclass"""

    def test_create_state_change(self):
        """Test creating a StateChange"""
        change = StateChange(
            entity_type="dns_host",
            name="server1.lan",
            change_type=ChangeType.CREATE,
            desired=Host(hostname="server1", domain="lan", server="192.168.1.100")
        )
        self.assertEqual(change.entity_type, "dns_host")
        self.assertEqual(change.name, "server1.lan")
        self.assertEqual(change.change_type, ChangeType.CREATE)
        self.assertIsNone(change.current)
        self.assertIsNotNone(change.desired)

    def test_state_change_with_diff(self):
        """Test StateChange with diff information"""
        change = StateChange(
            entity_type="dns_host",
            name="server1.lan",
            change_type=ChangeType.UPDATE,
            diff={"server": ("192.168.1.100", "192.168.1.101")}
        )
        self.assertEqual(change.change_type, ChangeType.UPDATE)
        self.assertIn("server", change.diff)
        self.assertEqual(change.diff["server"], ("192.168.1.100", "192.168.1.101"))


class TestDnsHostHandler(unittest.TestCase):
    """Test DnsHostHandler"""

    def setUp(self):
        self.handler = DnsHostHandler()

    def test_entity_type(self):
        """Test entity type identifier"""
        self.assertEqual(self.handler.entity_type, "dns_host")

    def test_primary_key(self):
        """Test primary key field"""
        self.assertEqual(self.handler.primary_key, "hostname")

    def test_secondary_keys(self):
        """Test secondary key fields"""
        self.assertIn("server", self.handler.secondary_keys)

    def test_get_primary_key_value(self):
        """Test composite key generation"""
        host = Host(hostname="server1", domain="lan", server="192.168.1.100")
        key = self.handler.get_primary_key_value(host)
        self.assertEqual(key, "server1.lan")

    def test_create_entity(self):
        """Test entity creation"""
        entity = self.handler.create_entity(
            hostname="server1",
            domain="lan",
            server="192.168.1.100",
            description="Test server"
        )
        self.assertIsInstance(entity, Host)
        self.assertEqual(entity.hostname, "server1")
        self.assertEqual(entity.domain, "lan")
        self.assertEqual(entity.server, "192.168.1.100")
        self.assertEqual(entity.description, "Test server")
        self.assertTrue(entity.enabled)

    def test_match_exact(self):
        """Test exact primary key matching"""
        desired = Host(hostname="server1", domain="lan", server="192.168.1.100")
        actual_list = [
            Host(hostname="server2", domain="lan", server="192.168.1.101"),
            Host(hostname="server1", domain="lan", server="192.168.1.100"),
        ]

        match_type, matched, alternatives = self.handler.match(desired, actual_list)
        self.assertEqual(match_type, "exact")
        self.assertIsNotNone(matched)
        self.assertEqual(matched.hostname, "server1")

    def test_match_none(self):
        """Test no match found"""
        desired = Host(hostname="server1", domain="lan", server="192.168.1.100")
        actual_list = [
            Host(hostname="server2", domain="lan", server="192.168.1.101"),
        ]

        match_type, matched, alternatives = self.handler.match(desired, actual_list)
        self.assertEqual(match_type, "none")
        self.assertIsNone(matched)

    def test_match_secondary(self):
        """Test secondary key matching by IP"""
        desired = Host(hostname="newname", domain="lan", server="192.168.1.100")
        actual_list = [
            Host(hostname="server1", domain="lan", server="192.168.1.100"),
        ]

        match_type, matched, alternatives = self.handler.match(desired, actual_list)
        self.assertEqual(match_type, "secondary")
        self.assertIsNotNone(matched)

    def test_compute_diff_no_changes(self):
        """Test diff with identical entities"""
        desired = Host(hostname="server1", domain="lan", server="192.168.1.100")
        actual = Host(hostname="server1", domain="lan", server="192.168.1.100")

        diff = self.handler.compute_diff(desired, actual)
        self.assertEqual(len(diff), 0)

    def test_compute_diff_with_changes(self):
        """Test diff with different IP"""
        desired = Host(hostname="server1", domain="lan", server="192.168.1.101")
        actual = Host(hostname="server1", domain="lan", server="192.168.1.100")

        diff = self.handler.compute_diff(desired, actual)
        self.assertIn("server", diff)
        self.assertEqual(diff["server"], ("192.168.1.100", "192.168.1.101"))


class TestDhcpReservationHandler(unittest.TestCase):
    """Test DhcpReservationHandler"""

    def setUp(self):
        self.handler = DhcpReservationHandler()

    def test_entity_type(self):
        """Test entity type identifier"""
        self.assertEqual(self.handler.entity_type, "dhcp_reservation")

    def test_primary_key(self):
        """Test primary key field"""
        self.assertEqual(self.handler.primary_key, "hw_address")

    def test_secondary_keys(self):
        """Test secondary key fields"""
        self.assertIn("ip_address", self.handler.secondary_keys)
        self.assertIn("hostname", self.handler.secondary_keys)

    def test_create_entity(self):
        """Test entity creation"""
        entity = self.handler.create_entity(
            hw_address="AA:BB:CC:DD:EE:FF",
            ip_address="192.168.1.50",
            hostname="printer"
        )
        self.assertIsInstance(entity, Reservation)
        self.assertEqual(entity.hw_address, "aa:bb:cc:dd:ee:ff")  # Normalized to lowercase
        self.assertEqual(entity.ip_address, "192.168.1.50")
        self.assertEqual(entity.hostname, "printer")

    def test_mac_address_normalization(self):
        """Test MAC address case normalization"""
        desired = Reservation(hw_address="AA:BB:CC:DD:EE:FF", ip_address="192.168.1.50")
        actual_list = [
            Reservation(hw_address="aa:bb:cc:dd:ee:ff", ip_address="192.168.1.50"),
        ]

        match_type, matched, alternatives = self.handler.match(desired, actual_list)
        self.assertEqual(match_type, "exact")


class TestFirewallAliasHandler(unittest.TestCase):
    """Test FirewallAliasHandler"""

    def setUp(self):
        self.handler = FirewallAliasHandler()

    def test_entity_type(self):
        """Test entity type identifier"""
        self.assertEqual(self.handler.entity_type, "firewall_alias")

    def test_primary_key(self):
        """Test primary key field"""
        self.assertEqual(self.handler.primary_key, "name")

    def test_create_entity(self):
        """Test entity creation"""
        entity = self.handler.create_entity(
            name="webservers",
            type="host",
            content=["10.0.0.1", "10.0.0.2"],
            description="Web server IPs"
        )
        self.assertIsInstance(entity, Alias)
        self.assertEqual(entity.name, "webservers")
        self.assertEqual(entity.type, Alias.AliasesAliasTypeEnum.HOST)
        self.assertEqual(entity.content, "10.0.0.1\n10.0.0.2")
        self.assertEqual(entity.description, "Web server IPs")

    def test_match_by_name(self):
        """Test exact match by name"""
        desired = Alias(name="webservers", type=Alias.AliasesAliasTypeEnum.HOST, content="10.0.0.1")
        actual_list = [
            Alias(name="webservers", type=Alias.AliasesAliasTypeEnum.HOST, content="10.0.0.1"),
        ]

        match_type, matched, alternatives = self.handler.match(desired, actual_list)
        self.assertEqual(match_type, "exact")

    def test_normalize_content(self):
        """Test content normalization for comparison"""
        content1 = self.handler._normalize_content("10.0.0.1\n10.0.0.2")
        content2 = self.handler._normalize_content(["10.0.0.1", "10.0.0.2"])

        self.assertEqual(content1, content2)
        self.assertEqual(content1, {"10.0.0.1", "10.0.0.2"})


class TestStateManager(unittest.TestCase):
    """Test StateManager"""

    def setUp(self):
        self.mock_client = Mock()
        # Mock search results
        self.mock_client.unbound_search_host_override.return_value = Mock(rows=[])
        self.mock_client.kea_dhcpv4_search_reservation.return_value = Mock(rows=[])
        self.mock_client.firewall_alias_search_item.return_value = Mock(rows=[])

    def test_init(self):
        """Test StateManager initialization"""
        state = StateManager(self.mock_client)
        self.assertIsNotNone(state._handlers)
        self.assertIn("dns_host", state._handlers)
        self.assertIn("dhcp_reservation", state._handlers)
        self.assertIn("firewall_alias", state._handlers)

    def test_dns_host_fluent_api(self):
        """Test fluent API for DNS host"""
        state = StateManager(self.mock_client)
        result = state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        self.assertIs(result, state)  # Returns self for chaining
        self.assertEqual(len(state._desired_state.get("dns_host", [])), 1)

    def test_dhcp_reservation_fluent_api(self):
        """Test fluent API for DHCP reservation"""
        state = StateManager(self.mock_client)
        result = state.dhcp_reservation(mac="aa:bb:cc:dd:ee:ff", ip="192.168.1.50")

        self.assertIs(result, state)
        self.assertEqual(len(state._desired_state.get("dhcp_reservation", [])), 1)

    def test_firewall_alias_fluent_api(self):
        """Test fluent API for firewall alias"""
        state = StateManager(self.mock_client)
        result = state.firewall_alias(name="webservers", type="host", content=["10.0.0.1"])

        self.assertIs(result, state)
        self.assertEqual(len(state._desired_state.get("firewall_alias", [])), 1)

    def test_chained_calls(self):
        """Test chained fluent API calls"""
        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100") \
             .dns_host(hostname="server2", domain="lan", ip="192.168.1.101") \
             .dhcp_reservation(mac="aa:bb:cc:dd:ee:ff", ip="192.168.1.50")

        self.assertEqual(len(state._desired_state.get("dns_host", [])), 2)
        self.assertEqual(len(state._desired_state.get("dhcp_reservation", [])), 1)

    def test_plan_create(self):
        """Test plan detects CREATE needed"""
        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        changes = state.plan()

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, ChangeType.CREATE)
        self.assertEqual(changes[0].entity_type, "dns_host")
        self.assertEqual(changes[0].name, "server1.lan")

    def test_plan_match(self):
        """Test plan detects MATCH (no changes needed)"""
        # Setup mock to return existing host
        existing_host = Host(hostname="server1", domain="lan", server="192.168.1.100")
        self.mock_client.unbound_search_host_override.return_value = Mock(rows=[existing_host])

        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        changes = state.plan()

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, ChangeType.MATCH)

    def test_plan_update(self):
        """Test plan detects UPDATE needed"""
        # Setup mock to return existing host with different IP
        existing_host = Host(
            hostname="server1",
            domain="lan",
            server="192.168.1.99"  # Different IP
        )
        # Add uuid manually since from_ui_dict usually does this
        object.__setattr__(existing_host, 'uuid', UUID("12345678-1234-5678-9abc-def012345678"))
        self.mock_client.unbound_search_host_override.return_value = Mock(rows=[existing_host])

        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        changes = state.plan()

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, ChangeType.UPDATE)
        self.assertIn("server", changes[0].diff)
        self.assertEqual(changes[0].diff["server"], ("192.168.1.99", "192.168.1.100"))

    def test_plan_ambiguous(self):
        """Test plan detects AMBIGUOUS match"""
        # Setup mock to return multiple hosts with same IP but different names
        host1 = Host(hostname="host1", domain="lan", server="192.168.1.100")
        host2 = Host(hostname="host2", domain="lan", server="192.168.1.100")
        self.mock_client.unbound_search_host_override.return_value = Mock(rows=[host1, host2])

        state = StateManager(self.mock_client)
        # Use different hostname but same IP - triggers secondary key ambiguity
        state.dns_host(hostname="newhost", domain="lan", ip="192.168.1.100")

        changes = state.plan()

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, ChangeType.AMBIGUOUS)
        self.assertEqual(len(changes[0].alternatives), 2)

    def test_clear_cache(self):
        """Test cache clearing"""
        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")
        state.plan()  # Populates cache

        self.assertIn("dns_host", state._actual_cache)

        state.clear_cache()

        self.assertEqual(len(state._actual_cache), 0)

    def test_clear_desired(self):
        """Test clearing desired state"""
        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        self.assertEqual(len(state._desired_state), 1)

        state.clear_desired()

        self.assertEqual(len(state._desired_state), 0)

    def test_format_plan(self):
        """Test plan formatting"""
        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        output = state.format_plan()

        self.assertIn("State Plan:", output)
        self.assertIn("To create", output)
        self.assertIn("dns_host", output)
        self.assertIn("server1.lan", output)

    def test_apply_auto_approve(self):
        """Test apply with auto_approve"""
        self.mock_client.unbound_add_host_override.return_value = Mock(result="saved")

        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        applied = state.apply(auto_approve=True)

        self.assertEqual(len(applied), 1)
        self.mock_client.unbound_add_host_override.assert_called_once()

    def test_apply_with_callback(self):
        """Test apply with custom callback"""
        self.mock_client.unbound_add_host_override.return_value = Mock(result="saved")

        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        callback_called = []

        def on_change(change, auto_approve):
            callback_called.append(change)
            return True  # Approve the change

        applied = state.apply(on_change=on_change)

        self.assertEqual(len(callback_called), 1)
        self.assertEqual(len(applied), 1)

    def test_apply_skips_without_approval(self):
        """Test apply skips changes without approval"""
        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        applied = state.apply(auto_approve=False)

        self.assertEqual(len(applied), 0)
        self.mock_client.unbound_add_host_override.assert_not_called()

    def test_plan_detect_deletes(self):
        """Test plan detects DELETE when entity exists but not in desired state"""
        # Setup mock to return existing hosts
        host1 = Host(hostname="server1", domain="lan", server="192.168.1.100")
        host2 = Host(hostname="server2", domain="lan", server="192.168.1.101")
        host1.uuid = UUID("11111111-1111-1111-1111-111111111111")
        host2.uuid = UUID("22222222-2222-2222-2222-222222222222")
        self.mock_client.unbound_search_host_override.return_value = Mock(rows=[host1, host2])

        state = StateManager(self.mock_client)
        # Only declare server1 as desired - server2 should be flagged for delete
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        changes = state.plan(detect_deletes=True)

        # Should have 1 MATCH (server1) and 1 DELETE (server2)
        matches = [c for c in changes if c.change_type == ChangeType.MATCH]
        deletes = [c for c in changes if c.change_type == ChangeType.DELETE]

        self.assertEqual(len(matches), 1)
        self.assertEqual(len(deletes), 1)
        self.assertEqual(deletes[0].name, "server2.lan")
        self.assertEqual(deletes[0].uuid, "22222222-2222-2222-2222-222222222222")

    def test_apply_deletes_skipped_by_default(self):
        """Test apply skips deletes by default"""
        host1 = Host(hostname="server1", domain="lan", server="192.168.1.100")
        host1.uuid = UUID("11111111-1111-1111-1111-111111111111")
        host2 = Host(hostname="orphan", domain="lan", server="192.168.1.200")
        host2.uuid = UUID("22222222-2222-2222-2222-222222222222")
        self.mock_client.unbound_search_host_override.return_value = Mock(rows=[host1, host2])

        state = StateManager(self.mock_client)
        # Only server1 in desired state - orphan would be deleted but skipped
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        applied = state.apply(auto_approve=True, detect_deletes=True)

        # Should have no deletes (skipped by default), only matches
        deletes = [c for c in applied if c.change_type == ChangeType.DELETE]
        self.assertEqual(len(deletes), 0)
        self.mock_client.unbound_del_host_override.assert_not_called()

    def test_apply_deletes_when_enabled(self):
        """Test apply performs deletes when enabled"""
        host1 = Host(hostname="server1", domain="lan", server="192.168.1.100")
        host1.uuid = UUID("11111111-1111-1111-1111-111111111111")
        host2 = Host(hostname="orphan", domain="lan", server="192.168.1.200")
        host2.uuid = UUID("22222222-2222-2222-2222-222222222222")
        self.mock_client.unbound_search_host_override.return_value = Mock(rows=[host1, host2])
        self.mock_client.unbound_del_host_override.return_value = Mock(result="deleted")

        state = StateManager(self.mock_client)
        # Only server1 in desired state - orphan should be deleted
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        applied = state.apply(auto_approve=True, detect_deletes=True, skip_deletes=False)

        # Should have deleted orphan (server1 matches so not deleted)
        deletes = [c for c in applied if c.change_type == ChangeType.DELETE]
        self.assertEqual(len(deletes), 1)
        self.assertEqual(deletes[0].name, "orphan.lan")
        self.mock_client.unbound_del_host_override.assert_called_once()

    def test_format_plan_with_deletes(self):
        """Test format_plan shows deletes"""
        host1 = Host(hostname="orphan", domain="lan", server="192.168.1.200")
        host1.uuid = UUID("11111111-1111-1111-1111-111111111111")
        self.mock_client.unbound_search_host_override.return_value = Mock(rows=[host1])

        state = StateManager(self.mock_client)
        state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")

        changes = state.plan(detect_deletes=True)
        output = state.format_plan(changes)

        self.assertIn("To delete", output)
        self.assertIn("orphan.lan", output)

    def test_export(self):
        """Test export generates Python code"""
        host1 = Host(hostname="server1", domain="lan", server="192.168.1.100", description="Test")
        self.mock_client.unbound_search_host_override.return_value = Mock(rows=[host1])
        self.mock_client.kea_dhcpv4_search_reservation.return_value = Mock(rows=[])
        self.mock_client.firewall_alias_search_item.return_value = Mock(rows=[])

        state = StateManager(self.mock_client)
        code = state.export(['dns_host'])

        self.assertIn("state.dns_host(", code)
        self.assertIn("hostname='server1'", code)
        self.assertIn("domain='lan'", code)
        self.assertIn("ip='192.168.1.100'", code)


class TestEntityHandlerBase(unittest.TestCase):
    """Test EntityHandler base class functionality"""

    def test_get_uuid(self):
        """Test UUID extraction"""
        handler = DnsHostHandler()
        host = Host(hostname="test", domain="lan", server="192.168.1.1")

        uuid = handler.get_uuid(host)
        self.assertIsNone(uuid)  # No UUID set

    def test_normalize_value(self):
        """Test value normalization"""
        handler = DnsHostHandler()

        self.assertIsNone(handler._normalize_value(None))
        self.assertIsNone(handler._normalize_value(""))
        self.assertIsNone(handler._normalize_value([]))
        self.assertEqual(handler._normalize_value("test"), "test")
        self.assertEqual(handler._normalize_value(["a", "b"]), ["a", "b"])


if __name__ == '__main__':
    unittest.main()
