import unittest
from opnsense_api.pydantic.KeaDhcpv4 import (
    Subnet4, Reservation, Peer, PeerRoleEnum
)


class TestSubnet4(unittest.TestCase):
    """Test Subnet4 model parsing and serialization"""

    def setUp(self):
        # Default response from API (get_subnet without uuid)
        self.default_response = {
            "subnet4": {
                "subnet": "",
                "next_server": "",
                "option_data_autocollect": "1",
                "match-client-id": "1",
                "pools": "",
                "description": ""
            }
        }
        # Response from search_subnet with data
        self.search_row = {
            "uuid": "9a49bd56-8f52-467e-be2c-df747475bf8e",
            "subnet": "10.200.0.0/24",
            "next_server": "",
            "option_data_autocollect": "1",
            "match-client-id": "1",
            "pools": "10.200.0.100-10.200.0.200",
            "description": "Test Subnet from API"
        }

    def test_parse_defaults(self):
        """Test parsing default subnet response"""
        subnet = Subnet4.from_ui_dict(self.default_response)
        self.assertIsNone(subnet.subnet)
        self.assertIsNone(subnet.next_server)
        self.assertTrue(subnet.option_data_autocollect)
        self.assertTrue(subnet.match_client_id)
        self.assertIsNone(subnet.pools)
        self.assertIsNone(subnet.description)

    def test_parse_search_row(self):
        """Test parsing subnet from search result"""
        subnet = Subnet4.from_ui_dict(self.search_row)
        self.assertEqual(subnet.subnet, "10.200.0.0/24")
        self.assertEqual(subnet.pools, "10.200.0.100-10.200.0.200")
        self.assertEqual(subnet.description, "Test Subnet from API")
        self.assertEqual(str(subnet.uuid), "9a49bd56-8f52-467e-be2c-df747475bf8e")

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        subnet = Subnet4(
            subnet="10.100.0.0/24",
            pools="10.100.0.100-10.100.0.200",
            description="Test Subnet"
        )
        data = subnet.to_simple_dict()
        self.assertIn("subnet4", data)
        self.assertEqual(data["subnet4"]["subnet"], "10.100.0.0/24")
        self.assertEqual(data["subnet4"]["pools"], "10.100.0.100-10.100.0.200")
        self.assertEqual(data["subnet4"]["description"], "Test Subnet")
        # Check alias is used
        self.assertEqual(data["subnet4"]["match-client-id"], "1")
        self.assertNotIn("match_client_id", data["subnet4"])

    def test_boolean_serialization(self):
        """Test that booleans are serialized as '0'/'1'"""
        subnet = Subnet4(
            subnet="10.0.0.0/24",
            option_data_autocollect=False,
            match_client_id=False
        )
        data = subnet.to_simple_dict()
        self.assertEqual(data["subnet4"]["option_data_autocollect"], "0")
        self.assertEqual(data["subnet4"]["match-client-id"], "0")

    def test_roundtrip(self):
        """Test serialize then deserialize"""
        original = Subnet4(
            subnet="10.50.0.0/24",
            pools="10.50.0.10-10.50.0.100",
            description="Roundtrip Test",
            option_data_autocollect=True,
            match_client_id=False
        )
        data = original.to_simple_dict()
        restored = Subnet4.from_basic_dict(data)
        self.assertEqual(restored.subnet, original.subnet)
        self.assertEqual(restored.pools, original.pools)
        self.assertEqual(restored.description, original.description)
        self.assertEqual(restored.option_data_autocollect, original.option_data_autocollect)
        self.assertEqual(restored.match_client_id, original.match_client_id)


class TestReservation(unittest.TestCase):
    """Test Reservation model parsing and serialization"""

    def setUp(self):
        self.default_response = {
            "reservation": {
                "subnet": [],
                "ip_address": "",
                "hw_address": "",
                "hostname": "",
                "description": ""
            }
        }
        self.reservation_data = {
            "uuid": "abc12345-1234-5678-9abc-def012345678",
            "subnet": "9a49bd56-8f52-467e-be2c-df747475bf8e",
            "ip_address": "10.200.0.50",
            "hw_address": "00:11:22:33:44:55",
            "hostname": "test-host",
            "description": "Test Reservation"
        }

    def test_parse_defaults(self):
        """Test parsing default reservation response"""
        res = Reservation.from_ui_dict(self.default_response)
        self.assertIsNone(res.subnet)
        self.assertIsNone(res.ip_address)
        self.assertIsNone(res.hw_address)
        self.assertIsNone(res.hostname)
        self.assertIsNone(res.description)

    def test_parse_reservation(self):
        """Test parsing reservation data"""
        res = Reservation.from_ui_dict(self.reservation_data)
        self.assertEqual(res.ip_address, "10.200.0.50")
        self.assertEqual(res.hw_address, "00:11:22:33:44:55")
        self.assertEqual(res.hostname, "test-host")
        self.assertEqual(res.description, "Test Reservation")

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        res = Reservation(
            subnet="9a49bd56-8f52-467e-be2c-df747475bf8e",
            ip_address="10.200.0.60",
            hw_address="AA:BB:CC:DD:EE:FF",
            hostname="my-host",
            description="My Reservation"
        )
        data = res.to_simple_dict()
        self.assertIn("reservation", data)
        self.assertEqual(data["reservation"]["ip_address"], "10.200.0.60")
        self.assertEqual(data["reservation"]["hw_address"], "AA:BB:CC:DD:EE:FF")
        self.assertEqual(data["reservation"]["hostname"], "my-host")


class TestPeer(unittest.TestCase):
    """Test Peer model parsing and serialization"""

    def setUp(self):
        self.default_response = {
            "peer": {
                "name": "",
                "role": {
                    "primary": {"value": "primary", "selected": 1},
                    "standby": {"value": "standby", "selected": 0}
                },
                "url": ""
            }
        }
        self.peer_data = {
            "uuid": "12345678-1234-5678-9abc-def012345678",
            "name": "ha-peer-1",
            "role": "standby",
            "url": "http://10.0.0.2:8080/"
        }

    def test_parse_defaults(self):
        """Test parsing default peer response"""
        peer = Peer.from_ui_dict(self.default_response)
        self.assertIsNone(peer.name)
        self.assertEqual(peer.role, PeerRoleEnum.PRIMARY)
        self.assertIsNone(peer.url)

    def test_parse_peer(self):
        """Test parsing peer data"""
        peer = Peer.from_ui_dict(self.peer_data)
        self.assertEqual(peer.name, "ha-peer-1")
        self.assertEqual(peer.role, PeerRoleEnum.STANDBY)
        self.assertEqual(peer.url, "http://10.0.0.2:8080/")

    def test_serialize_to_simple_dict(self):
        """Test serialization to API format"""
        peer = Peer(
            name="my-peer",
            role=PeerRoleEnum.STANDBY,
            url="http://192.168.1.1:8080/"
        )
        data = peer.to_simple_dict()
        self.assertIn("peer", data)
        self.assertEqual(data["peer"]["name"], "my-peer")
        self.assertEqual(data["peer"]["role"], "standby")
        self.assertEqual(data["peer"]["url"], "http://192.168.1.1:8080/")

    def test_role_enum_values(self):
        """Test role enum has correct values"""
        self.assertEqual(PeerRoleEnum.PRIMARY.value, "primary")
        self.assertEqual(PeerRoleEnum.STANDBY.value, "standby")


if __name__ == '__main__':
    unittest.main()
