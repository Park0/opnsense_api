from unittest import TestCase
import json
from opnsense_api.pydantic.Server import Server


class TestPydanticServer(TestCase):

    @staticmethod
    def data_server_full_1():
        return r'{"server":{"id":"680b4fe1883731.32556700","enabled":"1","name":"realservername","description":"realserverdescription","address":"192.168.1.1","port":"8080","checkport":"","mode":{"":{"value":"None","selected":0},"active":{"value":"active [default]","selected":1},"backup":{"value":"backup","selected":0},"disabled":{"value":"disabled","selected":0}},"multiplexer_protocol":{"":{"value":"None","selected":0},"unspecified":{"value":"auto-selection [recommended]","selected":1},"fcgi":{"value":"FastCGI","selected":0},"h2":{"value":"HTTP\/2","selected":0},"h1":{"value":"HTTP\/1.1","selected":0}},"type":{"static":{"value":"static","selected":1},"template":{"value":"template","selected":0},"unix":{"value":"unix socket","selected":0}},"serviceName":"","number":"","linkedResolver":{"":{"value":"None","selected":1}},"resolverOpts":{"allow-dup-ip":{"value":"allow-dup-ip","selected":0},"ignore-weight":{"value":"ignore-weight","selected":0},"prevent-dup-ip":{"value":"prevent-dup-ip","selected":0}},"resolvePrefer":{"":{"value":"None","selected":1},"ipv4":{"value":"prefer IPv4","selected":0},"ipv6":{"value":"prefer IPv6 [default]","selected":0}},"ssl":"0","sslSNI":"","sslVerify":"1","sslCA":{"679dec55f3a64":{"value":"Example CA","selected":0},"679dfa5a00074":{"value":"ExampleCA Intermediate CA 2025 (ACME Client)","selected":0},"66635441877c1":{"value":"VPN 2024","selected":0}},"sslCRL":{"":{"value":"","selected":1}},"sslClientCertificate":{"":{"value":"None","selected":1},"675d8e013920d":{"value":"dune60c585","selected":0},"66636c95283d1":{"value":"HPT630 2024","selected":0},"66c8f4b4d7cf6":{"value":"huub820g4india","selected":0},"66c9ed00ee302":{"value":"huubs9","selected":0},"66c9f245233d3":{"value":"ignas9","selected":0},"6779103ceca0b":{"value":"mm-frigate vpn","selected":0},"6676b0a67c9e8":{"value":"MXQ01","selected":0},"666616383dcf7":{"value":"parkodap 2024","selected":0},"6665996d6014f":{"value":"parkos22","selected":0},"6665753d5cfd4":{"value":"testhost","selected":0},"67a5e34d10086":{"value":"rene-laptop-1 2025 vpn certificate","selected":0},"67a5e0615d35b":{"value":"Rene Beemer 2025 laptop-1","selected":0},"666758edcb605":{"value":"stefan-van-bohemen-windows-11 2024","selected":0},"669102c4486f9":{"value":"tamara 2024","selected":0},"66646f9e9c0ea":{"value":"TM-1212","selected":0},"679dfa5a08e3a":{"value":"vpn.example.lan (ACME Client)","selected":0},"666354e39adc7":{"value":"VPN server 2024","selected":0},"663794b8efb60":{"value":"Web GUI TLS certificate","selected":0}},"maxConnections":"","weight":"","checkInterval":"","checkDownInterval":"","source":"","advanced":"","unix_socket":{"":{"value":"None","selected":1}}}}'

    @staticmethod
    def data_server_basic_1():
        return r'{"server":{"enabled":"1","name":"realservername","description":"realserverdescription","type":"static","address":"192.168.1.1","serviceName":"","number":"","linkedResolver":"","resolverOpts":"","unix_socket":"","port":"8080","mode":"active","multiplexer_protocol":"unspecified","resolvePrefer":"","ssl":"0","sslSNI":"","sslVerify":"1","sslCA":"","sslCRL":"","sslClientCertificate":"","maxConnections":"","weight":"","checkInterval":"","checkDownInterval":"","checkport":"","source":"","advanced":""}}'

    def test_load_server(self):
        server_json = json.loads(self.data_server_full_1())
        server = Server.from_ui_dict(server_json) # type: Server

        server_basic_json = json.loads(self.data_server_basic_1())
        server_basic = Server.from_basic_dict(server_basic_json) # type: Server

        self.assertEqual(server_basic.to_simple_dict(), server.to_simple_dict())
