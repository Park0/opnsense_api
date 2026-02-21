import unittest
from opnsense_api.pydantic.InterfaceOverview import (
    Interface, InterfaceOverview, InterfaceExport, StatusEnum, LinkTypeEnum,
    InterfaceStatistics, InterfaceConfig, Nd6
)


class TestInterfaceOverview(unittest.TestCase):

    def setUp(self):
        self.api_response = [
            {"flags":["up","broadcast","running","simplex","multicast","lower_up"],"capabilities":["rxcsum","txcsum","vlan_mtu","vlan_hwtagging","jumbo_mtu","vlan_hwcsum","tso4","tso6","lro","vlan_hwfilter","vlan_hwtso","netmap","rxcsum_ipv6","txcsum_ipv6","hwstats","mextpg"],"options":["vlan_mtu","jumbo_mtu","hwstats","mextpg"],"macaddr":"00:0c:29:d4:f2:69","supported_media":["autoselect"],"is_physical":True,"device":"vmx0","mtu":"1500","macaddr_hw":"00:0c:29:d4:f2:69","media":"Ethernet autoselect","media_raw":"Ethernet autoselect","status":"up","nd6":{"flags":["performnud","ifdisabled","auto_linklocal"]},"statistics":{"device":"vmx0","driver":"vmx0","index":"1","flags":"8843","promiscuous listeners":"0","send queue length":"0","send queue max length":"50","send queue drops":"0","type":"Ethernet","address length":"6","header length":"18","link state":"2","vhid":"0","datalen":"152","mtu":"1500","metric":"0","line rate":"10000000000 bit/s","packets received":"7127","input errors":"0","packets transmitted":"10545","output errors":"0","collisions":"0","bytes received":"2036965","bytes transmitted":"6555171","multicasts received":"34","multicasts transmitted":"0","input queue drops":"0","packets for unknown protocol":"0","HW offload capabilities":"0x0","uptime at attach or stat reset":"1"},"routes":["default","10.0.34.0/24"],"config":{"if":"vmx0","descr":"","enable":"1","spoofmac":"","blockbogons":"1","ipaddr":"dhcp","dhcphostname":"","alias-address":"","alias-subnet":"32","dhcprejectfrom":"","adv_dhcp_pt_timeout":"","adv_dhcp_pt_retry":"","adv_dhcp_pt_select_timeout":"","adv_dhcp_pt_reboot":"","adv_dhcp_pt_backoff_cutoff":"","adv_dhcp_pt_initial_interval":"","adv_dhcp_pt_values":"SavedCfg","adv_dhcp_send_options":"","adv_dhcp_request_options":"","adv_dhcp_required_options":"","adv_dhcp_option_modifiers":"","adv_dhcp_config_advanced":"","adv_dhcp_config_file_override":"","adv_dhcp_config_file_override_path":"","identifier":"wan"},"ifctl.nameserver":["10.0.34.254"],"ifctl.router":["10.0.34.254"],"ifctl.searchdomain":["example.lan"],"identifier":"wan","description":"WAN","enabled":True,"link_type":"dhcp","addr4":"10.0.34.250/24","addr6":"","ipv4":[{"ipaddr":"10.0.34.250/24"}],"vlan_tag":None,"gateways":["10.0.34.254"]},
            {"flags":["up","broadcast","running","simplex","multicast","lower_up"],"capabilities":["rxcsum","txcsum","vlan_mtu","vlan_hwtagging","jumbo_mtu","vlan_hwcsum","tso4","tso6","lro","vlan_hwfilter","vlan_hwtso","netmap","rxcsum_ipv6","txcsum_ipv6","hwstats","mextpg"],"options":["vlan_mtu","jumbo_mtu","hwstats","mextpg"],"macaddr":"00:0c:29:d4:f2:73","supported_media":["autoselect"],"is_physical":True,"device":"vmx1","mtu":"1500","macaddr_hw":"00:0c:29:d4:f2:73","media":"Ethernet autoselect","media_raw":"Ethernet autoselect","status":"up","nd6":{"flags":["performnud","auto_linklocal"]},"statistics":{"device":"vmx1","driver":"vmx1","index":"2","flags":"8843","promiscuous listeners":"0","send queue length":"0","send queue max length":"50","send queue drops":"0","type":"Ethernet","address length":"6","header length":"18","link state":"2","vhid":"0","datalen":"152","mtu":"1500","metric":"0","line rate":"10000000000 bit/s","packets received":"2","input errors":"0","packets transmitted":"3","output errors":"0","collisions":"0","bytes received":"120","bytes transmitted":"346","multicasts received":"0","multicasts transmitted":"3","input queue drops":"0","packets for unknown protocol":"0","HW offload capabilities":"0x0","uptime at attach or stat reset":"1"},"routes":["192.168.1.0/24","fe80::%vmx1/64"],"config":{"if":"vmx1","descr":"","enable":"1","spoofmac":"","ipaddr":"192.168.1.1","subnet":"24","ipaddrv6":"track6","track6-interface":"wan","track6-prefix-id":"0","identifier":"lan"},"identifier":"lan","description":"LAN","enabled":True,"link_type":"static","addr4":"192.168.1.1/24","addr6":"","ipv4":[{"ipaddr":"192.168.1.1/24"}],"ipv6":[{"ipaddr":"fe80::20c:29ff:fed4:f273/64"}],"vlan_tag":None,"gateways":[]},
            {"flags":["up","loopback","running","multicast","lower_up"],"capabilities":["rxcsum","txcsum","linkstate","rxcsum_ipv6","txcsum_ipv6"],"options":["rxcsum","txcsum","linkstate","rxcsum_ipv6","txcsum_ipv6"],"macaddr":"00:00:00:00:00:00","supported_media":[],"is_physical":False,"device":"lo0","mtu":"16384","groups":["lo"],"nd6":{"flags":["performnud","auto_linklocal"]},"statistics":{"device":"lo0","driver":"lo0","index":"3","flags":"8049","promiscuous listeners":"0","send queue length":"0","send queue max length":"50","send queue drops":"0","type":"Loopback","address length":"0","header length":"0","link state":"2","vhid":"0","datalen":"152","mtu":"16384","metric":"0","line rate":"0 bit/s","packets received":"2640","input errors":"0","packets transmitted":"2640","output errors":"0","collisions":"0","bytes received":"657591","bytes transmitted":"657591","multicasts received":"0","multicasts transmitted":"0","input queue drops":"0","packets for unknown protocol":"0","HW offload capabilities":"0xe0f","uptime at attach or stat reset":"2"},"routes":["10.0.34.250","127.0.0.1","192.168.1.1","::1","fe80::20c:29ff:fed4:f273%lo0","fe80::%lo0/64","fe80::1%lo0"],"config":{"internal_dynamic":"1","descr":"Loopback","enable":"1","if":"lo0","ipaddr":"127.0.0.1","ipaddrv6":"::1","subnet":"8","subnetv6":"128","type":"none","virtual":"1","identifier":"lo0"},"status":"up","identifier":"lo0","description":"Loopback","enabled":True,"link_type":"static","addr4":"127.0.0.1/8","addr6":"::1/128","ipv4":[{"ipaddr":"127.0.0.1/8"}],"ipv6":[{"ipaddr":"::1/128"},{"ipaddr":"fe80::1/64"}],"vlan_tag":None,"gateways":[]},
            {"flags":[],"capabilities":["capabilities="],"options":["options="],"macaddr":"00:00:00:00:00:00","ipv4":[],"ipv6":[],"supported_media":[],"is_physical":False,"device":"enc0","mtu":"1536","groups":["enc"],"nd6":{"flags":["performnud","ifdisabled","auto_linklocal"]},"statistics":{"device":"enc0","driver":"enc0","index":"4","flags":"0","promiscuous listeners":"0","send queue length":"0","send queue max length":"50","send queue drops":"0","type":"unknown type 244","address length":"0","header length":"0","link state":"0","vhid":"0","datalen":"152","mtu":"1536","metric":"0","line rate":"0 bit/s","packets received":"0","input errors":"0","packets transmitted":"0","output errors":"0","collisions":"0","bytes received":"0","bytes transmitted":"0","multicasts received":"0","multicasts transmitted":"0","input queue drops":"0","packets for unknown protocol":"0","HW offload capabilities":"0x0","uptime at attach or stat reset":"2"},"status":"down","identifier":"","description":"Unassigned Interface"},
            {"flags":[],"capabilities":["capabilities="],"options":["options="],"macaddr":"00:00:00:00:00:00","ipv4":[],"ipv6":[],"supported_media":[],"is_physical":False,"device":"pflog0","mtu":"33152","groups":["pflog"],"statistics":{"device":"pflog0","driver":"pflog0","index":"6","flags":"0","promiscuous listeners":"0","send queue length":"0","send queue max length":"50","send queue drops":"0","type":"unknown type 246","address length":"0","header length":"72","link state":"0","vhid":"0","datalen":"152","mtu":"33152","metric":"0","line rate":"0 bit/s","packets received":"0","input errors":"0","packets transmitted":"4008","output errors":"0","collisions":"0","bytes received":"0","bytes transmitted":"308724","multicasts received":"0","multicasts transmitted":"0","input queue drops":"0","packets for unknown protocol":"0","HW offload capabilities":"0x0","uptime at attach or stat reset":"2"},"status":"down","identifier":"","description":"Unassigned Interface"}
        ]

    def test_parse_wan_interface(self):
        """Test parsing WAN interface with DHCP"""
        iface = InterfaceOverview(**self.api_response[0])

        self.assertEqual(iface.identifier, "wan")
        self.assertEqual(iface.description, "WAN")
        self.assertEqual(iface.device, "vmx0")
        self.assertEqual(iface.status, StatusEnum.UP)
        self.assertEqual(iface.link_type, LinkTypeEnum.DHCP)
        self.assertEqual(iface.mtu, 1500)
        self.assertTrue(iface.enabled)
        self.assertTrue(iface.is_physical)
        self.assertEqual(iface.macaddr, "00:0c:29:d4:f2:69")
        self.assertEqual(iface.addr4, "10.0.34.250/24")
        self.assertEqual(iface.gateways, ["10.0.34.254"])
        self.assertEqual(iface.ifctl_nameserver, ["10.0.34.254"])
        self.assertIn("up", iface.flags)

    def test_parse_lan_interface(self):
        """Test parsing LAN interface with static IP"""
        iface = InterfaceOverview(**self.api_response[1])

        self.assertEqual(iface.identifier, "lan")
        self.assertEqual(iface.description, "LAN")
        self.assertEqual(iface.device, "vmx1")
        self.assertEqual(iface.status, StatusEnum.UP)
        self.assertEqual(iface.link_type, LinkTypeEnum.STATIC)
        self.assertEqual(iface.addr4, "192.168.1.1/24")
        self.assertTrue(iface.is_physical)
        self.assertEqual(len(iface.ipv4), 1)
        self.assertEqual(iface.ipv4[0].ipaddr, "192.168.1.1/24")

    def test_parse_loopback_interface(self):
        """Test parsing loopback interface"""
        iface = InterfaceOverview(**self.api_response[2])

        self.assertEqual(iface.identifier, "lo0")
        self.assertEqual(iface.description, "Loopback")
        self.assertEqual(iface.device, "lo0")
        self.assertEqual(iface.status, StatusEnum.UP)
        self.assertEqual(iface.mtu, 16384)
        self.assertFalse(iface.is_physical)
        self.assertEqual(iface.addr4, "127.0.0.1/8")
        self.assertEqual(iface.addr6, "::1/128")
        self.assertEqual(len(iface.ipv6), 2)
        self.assertIn("lo", iface.groups)

    def test_parse_down_interface(self):
        """Test parsing interface that is down"""
        iface = InterfaceOverview(**self.api_response[3])

        self.assertEqual(iface.device, "enc0")
        self.assertEqual(iface.status, StatusEnum.DOWN)
        self.assertFalse(iface.is_physical)
        self.assertEqual(iface.identifier, "")
        self.assertEqual(iface.description, "Unassigned Interface")
        self.assertIsNone(iface.link_type)

    def test_statistics_parsing(self):
        """Test that statistics are parsed with correct types"""
        iface = InterfaceOverview(**self.api_response[0])
        stats = iface.statistics

        self.assertIsNotNone(stats)
        self.assertEqual(stats.device, "vmx0")
        self.assertEqual(stats.index, 1)
        self.assertEqual(stats.packets_received, 7127)
        self.assertEqual(stats.packets_transmitted, 10545)
        self.assertEqual(stats.bytes_received, 2036965)
        self.assertEqual(stats.bytes_transmitted, 6555171)
        self.assertEqual(stats.input_errors, 0)
        self.assertEqual(stats.output_errors, 0)
        self.assertEqual(stats.mtu, 1500)
        self.assertEqual(stats.line_rate, "10000000000 bit/s")

    def test_config_parsing(self):
        """Test that interface config is parsed correctly"""
        iface = InterfaceOverview(**self.api_response[0])
        config = iface.config

        self.assertIsNotNone(config)
        self.assertEqual(config.interface, "vmx0")
        self.assertEqual(config.identifier, "wan")
        self.assertEqual(config.ipaddr, "dhcp")
        self.assertEqual(config.enable, "1")
        self.assertEqual(config.blockbogons, "1")

    def test_nd6_parsing(self):
        """Test that nd6 flags are parsed"""
        iface = InterfaceOverview(**self.api_response[0])

        self.assertIsNotNone(iface.nd6)
        self.assertIn("performnud", iface.nd6.flags)
        self.assertIn("auto_linklocal", iface.nd6.flags)

    def test_parse_all_interfaces(self):
        """Test parsing all interfaces from response"""
        interfaces = [InterfaceOverview(**data) for data in self.api_response]

        self.assertEqual(len(interfaces), 5)
        devices = [i.device for i in interfaces]
        self.assertIn("vmx0", devices)
        self.assertIn("vmx1", devices)
        self.assertIn("lo0", devices)
        self.assertIn("enc0", devices)
        self.assertIn("pflog0", devices)


class TestInterfaceExport(unittest.TestCase):
    """Test InterfaceExport collection with query methods"""

    def setUp(self):
        self.api_response = [
            {"flags":["up","broadcast","running","simplex","multicast","lower_up"],"capabilities":[],"options":[],"macaddr":"00:0c:29:d4:f2:69","supported_media":["autoselect"],"is_physical":True,"device":"vmx0","mtu":"1500","macaddr_hw":"00:0c:29:d4:f2:69","media":"Ethernet autoselect","status":"up","nd6":{"flags":[]},"statistics":{},"routes":[],"config":{"if":"vmx0","identifier":"wan"},"ifctl.nameserver":["10.0.34.254"],"identifier":"wan","description":"WAN","enabled":True,"link_type":"dhcp","addr4":"10.0.34.250/24","addr6":"","ipv4":[{"ipaddr":"10.0.34.250/24"}],"vlan_tag":None,"gateways":["10.0.34.254"]},
            {"flags":["up","broadcast","running"],"capabilities":[],"options":[],"macaddr":"00:0c:29:d4:f2:73","supported_media":["autoselect"],"is_physical":True,"device":"vmx1","mtu":"1500","status":"up","nd6":{"flags":[]},"statistics":{},"routes":[],"config":{"if":"vmx1","identifier":"lan"},"identifier":"lan","description":"LAN","enabled":True,"link_type":"static","addr4":"192.168.1.1/24","addr6":"","ipv4":[{"ipaddr":"192.168.1.1/24"}],"ipv6":[{"ipaddr":"fe80::20c:29ff:fed4:f273/64"}],"vlan_tag":None,"gateways":[],"groups":[]},
            {"flags":["up","loopback","running"],"capabilities":[],"options":[],"macaddr":"00:00:00:00:00:00","supported_media":[],"is_physical":False,"device":"lo0","mtu":"16384","groups":["lo"],"nd6":{"flags":[]},"statistics":{},"status":"up","identifier":"lo0","description":"Loopback","enabled":True,"link_type":"static","addr4":"127.0.0.1/8","addr6":"::1/128","ipv4":[{"ipaddr":"127.0.0.1/8"}],"ipv6":[{"ipaddr":"::1/128"}],"vlan_tag":None,"gateways":[]},
            {"flags":[],"capabilities":[],"options":[],"macaddr":"00:00:00:00:00:00","ipv4":[],"ipv6":[],"supported_media":[],"is_physical":False,"device":"enc0","mtu":"1536","groups":["enc"],"nd6":{"flags":[]},"statistics":{},"status":"down","identifier":"","description":"Unassigned Interface","enabled":False,"vlan_tag":None},
            {"flags":["up","broadcast"],"capabilities":[],"options":[],"macaddr":"00:0c:29:d4:f2:73","supported_media":[],"is_physical":False,"device":"vmx1_vlan100","mtu":"1500","groups":[],"nd6":{"flags":[]},"statistics":{},"status":"up","identifier":"opt1","description":"VLAN100","enabled":True,"link_type":"static","addr4":"10.100.0.1/24","vlan_tag":100,"gateways":[]}
        ]
        self.export = InterfaceExport.from_api_response(self.api_response)

    def test_from_api_response(self):
        """Test creating InterfaceExport from API response"""
        self.assertEqual(len(self.export), 5)
        self.assertIsInstance(self.export.interfaces[0], Interface)

    def test_iteration(self):
        """Test that InterfaceExport is iterable"""
        devices = [iface.device for iface in self.export]
        self.assertEqual(devices, ["vmx0", "vmx1", "lo0", "enc0", "vmx1_vlan100"])

    def test_indexing(self):
        """Test that InterfaceExport supports indexing"""
        self.assertEqual(self.export[0].device, "vmx0")
        self.assertEqual(self.export[-1].device, "vmx1_vlan100")

    def test_get_by_identifier(self):
        """Test getting interface by OPNsense identifier"""
        wan = self.export.get_by_identifier("wan")
        self.assertIsNotNone(wan)
        self.assertEqual(wan.device, "vmx0")

        lan = self.export.get_by_identifier("lan")
        self.assertIsNotNone(lan)
        self.assertEqual(lan.device, "vmx1")

        # Non-existent identifier
        self.assertIsNone(self.export.get_by_identifier("nonexistent"))

    def test_get_by_device(self):
        """Test getting interface by device name"""
        iface = self.export.get_by_device("vmx0")
        self.assertIsNotNone(iface)
        self.assertEqual(iface.identifier, "wan")

        iface = self.export.get_by_device("lo0")
        self.assertIsNotNone(iface)
        self.assertEqual(iface.identifier, "lo0")

        self.assertIsNone(self.export.get_by_device("nonexistent"))

    def test_get_by_description(self):
        """Test getting interface by description"""
        wan = self.export.get_by_description("WAN")
        self.assertIsNotNone(wan)
        self.assertEqual(wan.device, "vmx0")

        loopback = self.export.get_by_description("Loopback")
        self.assertIsNotNone(loopback)
        self.assertEqual(loopback.device, "lo0")

        self.assertIsNone(self.export.get_by_description("NonExistent"))

    def test_get_by_mac(self):
        """Test getting interface by MAC address"""
        iface = self.export.get_by_mac("00:0c:29:d4:f2:69")
        self.assertIsNotNone(iface)
        self.assertEqual(iface.identifier, "wan")

        # Case insensitive
        iface = self.export.get_by_mac("00:0C:29:D4:F2:69")
        self.assertIsNotNone(iface)
        self.assertEqual(iface.identifier, "wan")

        self.assertIsNone(self.export.get_by_mac("ff:ff:ff:ff:ff:ff"))

    def test_get_by_ip(self):
        """Test getting interface by IP address"""
        wan = self.export.get_by_ip("10.0.34.250")
        self.assertIsNotNone(wan)
        self.assertEqual(wan.identifier, "wan")

        lan = self.export.get_by_ip("192.168.1.1")
        self.assertIsNotNone(lan)
        self.assertEqual(lan.identifier, "lan")

        self.assertIsNone(self.export.get_by_ip("8.8.8.8"))

    def test_get_physical(self):
        """Test getting all physical interfaces"""
        physical = self.export.get_physical()
        self.assertEqual(len(physical), 2)
        devices = [i.device for i in physical]
        self.assertIn("vmx0", devices)
        self.assertIn("vmx1", devices)

    def test_get_virtual(self):
        """Test getting all virtual interfaces"""
        virtual = self.export.get_virtual()
        self.assertEqual(len(virtual), 3)
        devices = [i.device for i in virtual]
        self.assertIn("lo0", devices)
        self.assertIn("enc0", devices)
        self.assertIn("vmx1_vlan100", devices)

    def test_get_enabled(self):
        """Test getting all enabled interfaces"""
        enabled = self.export.get_enabled()
        self.assertEqual(len(enabled), 4)
        # enc0 is disabled
        devices = [i.device for i in enabled]
        self.assertNotIn("enc0", devices)

    def test_get_up(self):
        """Test getting all interfaces with status up"""
        up = self.export.get_up()
        self.assertEqual(len(up), 4)
        devices = [i.device for i in up]
        self.assertNotIn("enc0", devices)  # enc0 is down

    def test_get_down(self):
        """Test getting all interfaces with status down"""
        down = self.export.get_down()
        self.assertEqual(len(down), 1)
        self.assertEqual(down[0].device, "enc0")

    def test_get_by_vlan_tag(self):
        """Test getting interface by VLAN tag"""
        vlan = self.export.get_by_vlan_tag(100)
        self.assertIsNotNone(vlan)
        self.assertEqual(vlan.device, "vmx1_vlan100")
        self.assertEqual(vlan.identifier, "opt1")

        self.assertIsNone(self.export.get_by_vlan_tag(999))

    def test_get_vlans(self):
        """Test getting all VLAN interfaces"""
        vlans = self.export.get_vlans()
        self.assertEqual(len(vlans), 1)
        self.assertEqual(vlans[0].vlan_tag, 100)

    def test_get_assigned(self):
        """Test getting all assigned interfaces"""
        assigned = self.export.get_assigned()
        self.assertEqual(len(assigned), 4)
        identifiers = [i.identifier for i in assigned]
        self.assertIn("wan", identifiers)
        self.assertIn("lan", identifiers)
        self.assertIn("lo0", identifiers)
        self.assertIn("opt1", identifiers)

    def test_get_unassigned(self):
        """Test getting all unassigned interfaces"""
        unassigned = self.export.get_unassigned()
        self.assertEqual(len(unassigned), 1)
        self.assertEqual(unassigned[0].device, "enc0")

    def test_filter_by_group(self):
        """Test filtering interfaces by group"""
        loopback_group = self.export.filter_by_group("lo")
        self.assertEqual(len(loopback_group), 1)
        self.assertEqual(loopback_group[0].device, "lo0")

        enc_group = self.export.filter_by_group("enc")
        self.assertEqual(len(enc_group), 1)
        self.assertEqual(enc_group[0].device, "enc0")

        # Non-existent group
        self.assertEqual(len(self.export.filter_by_group("nonexistent")), 0)

    def test_filter_by_link_type(self):
        """Test filtering interfaces by link type"""
        dhcp = self.export.filter_by_link_type(LinkTypeEnum.DHCP)
        self.assertEqual(len(dhcp), 1)
        self.assertEqual(dhcp[0].identifier, "wan")

        static = self.export.filter_by_link_type(LinkTypeEnum.STATIC)
        self.assertEqual(len(static), 3)
        identifiers = [i.identifier for i in static]
        self.assertIn("lan", identifiers)
        self.assertIn("lo0", identifiers)

    def test_backwards_compatibility_alias(self):
        """Test that InterfaceOverview is alias for Interface"""
        self.assertIs(InterfaceOverview, Interface)


if __name__ == '__main__':
    unittest.main()
