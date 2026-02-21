import json
from unittest import TestCase
from opnsense_api.pydantic.Action import Action
from opnsense_api.pydantic.Frontend import Frontend
from opnsense_api.pydantic.Result import Result


class TestPydanticFrontend(TestCase):

    def test_load_action(self):
        action = Action.from_ui_dict(json.loads(self.data_action_full_1()))
        self.assertEqual(action.to_simple_dict(), Action.from_basic_dict(json.loads(self.data_action_basic_1())).to_simple_dict())
        action_full = Action.from_ui_dict(json.loads(self.data_action_full_1()))
        action_full.description = 'actiondescription'
        action_full.name = 'action'
        action_full.type = Action.ActionsActionTypeEnum.USE_BACKEND
        action_full.use_backend = '1bf97d05-d8a3-4e84-a061-9bb0c8643ff8'
        self.assertEqual(action_full.to_simple_dict(), Action.from_basic_dict(json.loads(self.data_action_basic_2())).to_simple_dict())


    def test_load_unload(self):
        frontend_full = self.data_frontend_full_1()
        frontend_basic = self.data_frontend_basic_1()

        frontend_full_json = json.loads(frontend_full)
        full = Frontend.from_ui_dict(frontend_full_json) # type: Frontend
        frontend_basic_json = json.loads(frontend_basic)
        basic = Frontend.from_basic_dict(frontend_basic_json) # type: Frontend
        self.assertEqual('frontend', full.name)
        self.assertEqual('frontend', basic.name)
        self.assertEqual(full.enabled, basic.enabled)
        self.assertEqual(full.description, basic.description)
        #elf.assertEqual(basic.bind, ",".join(str(v.value) for v in full.bind.values() if v.selected == 1))
        self.assertEqual(basic.bind, full.bind)
        self.assertEqual(basic.mode, full.mode)
        self.assertEqual(basic.defaultBackend, full.defaultBackend)

        full_basic = full.to_simple_dict()
        self.assertEqual(full_basic, basic.to_simple_dict())

        self.assertEqual(full.get_port(), '8043')

    def data_frontend_basic_1(self):
        frontend_basic = r"""
        {
  "frontend": {
    "enabled": "1",
    "name": "frontend",
    "description": "Frontend for server",
    "bind": "127.0.3.5:8043",
    "bindOptions": "",
    "mode": "http",
    "defaultBackend": "",
    "ssl_enabled": "0",
    "ssl_certificates": "",
    "ssl_default_certificate": "",
    "ssl_customOptions": "",
    "ssl_advancedEnabled": "0",
    "ssl_minVersion": "TLSv1.2",
    "ssl_maxVersion": "",
    "ssl_cipherList": "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256",
    "ssl_cipherSuites": "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256",
    "ssl_hstsEnabled": "1",
    "ssl_hstsIncludeSubDomains": "0",
    "ssl_hstsPreload": "0",
    "ssl_hstsMaxAge": "15768000",
    "ssl_bindOptions": "prefer-client-ciphers",
    "ssl_clientAuthEnabled": "0",
    "ssl_clientAuthVerify": "required",
    "ssl_clientAuthCAs": "",
    "ssl_clientAuthCRLs": "",
    "http2Enabled": "1",
    "http2Enabled_nontls": "0",
    "advertised_protocols": "h2,http11",
    "forwardFor": "0",
    "prometheus_enabled": "0",
    "prometheus_path": "/metrics",
    "connectionBehaviour": "http-keep-alive",
    "basicAuthEnabled": "0",
    "basicAuthUsers": "",
    "basicAuthGroups": "",
    "tuning_maxConnections": "",
    "tuning_timeoutClient": "",
    "tuning_timeoutHttpReq": "",
    "tuning_timeoutHttpKeepAlive": "",
    "linkedCpuAffinityRules": "",
    "tuning_shards": "",
    "logging_dontLogNull": "0",
    "logging_dontLogNormal": "0",
    "logging_logSeparateErrors": "0",
    "logging_detailedLog": "0",
    "logging_socketStats": "0",
    "stickiness_pattern": "",
    "stickiness_dataTypes": "",
    "stickiness_expire": "30m",
    "stickiness_size": "50k",
    "stickiness_counter": "1",
    "stickiness_counter_key": "src",
    "stickiness_length": "",
    "stickiness_connRatePeriod": "10s",
    "stickiness_sessRatePeriod": "10s",
    "stickiness_httpReqRatePeriod": "10s",
    "stickiness_httpErrRatePeriod": "10s",
    "stickiness_bytesInRatePeriod": "1m",
    "stickiness_bytesOutRatePeriod": "1m",
    "customOptions": "",
    "linkedActions": "4ad4fb72-d9cf-4b87-b5d3-434daffc46e3,66678189-587b-4359-bfad-a7536ec9d048",
    "linkedErrorfiles": ""
  }
}
        """
        return frontend_basic

    def data_frontend_full_1(self):
        frontend_full = r"""
{
          "frontend": {
            "id": "6811d8617f60c4.20687329",
            "enabled": "1",
            "name": "frontend",
            "description": "Frontend for server",
            "bind": {
              "127.0.3.5:8043": {
                "value": "127.0.3.5:8043",
                "selected": 1
              }
            },
            "bindOptions": "",
            "mode": {
              "http": {
                "value": "HTTP \/ HTTPS (SSL offloading) [default]",
                "selected": 1
              },
              "ssl": {
                "value": "SSL \/ HTTPS (TCP mode)",
                "selected": 0
              },
              "tcp": {
                "value": "TCP",
                "selected": 0
              }
            },
            "defaultBackend": {
              "": {
                "value": "None",
                "selected": 1
              },
              "dbf96fa2-23e3-4808-9a4b-4cc52367c987": {
                "value": "backendexample2_dot_lan",
                "selected": 0
              },
              "cfc0cc6d-e0a1-4c82-8c20-d769bcaaec00": {
                "value": "backendexample2_dot_lan",
                "selected": 0
              },
              "17712ab3-b15b-4e5f-a43a-742898a954ab": {
                "value": "backendexample2_dot_lan",
                "selected": 0
              },
              "6695a64f-dc63-4dca-9eb0-70289e349492": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "524397c1-fb82-4d8b-97b9-39d8b470f4cf": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "a4055548-7bfb-4b62-9dee-ec07fd6b32e8": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "325cb27b-f075-48f8-8320-26a0bd5b58b4": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "09584ef8-6ec3-4c24-9e58-c40623239b15": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "85e0ef77-caea-43d5-84dc-92e27d0d591f": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "0bda6418-3e83-4a2c-b846-936c59b785c9": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "d3b90ffc-383e-4e1a-b940-90fa4a38d724": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "cdf6b3ca-4533-4588-bb30-d6f94db3239d": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "ed772e76-84fa-4cdb-8565-f8b2bdf9ebbe": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "dbc6378f-8ca7-4c48-a625-db235b2a083f": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "fefb021a-6477-4a3a-8348-556ebee69cd8": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "e4b15b31-f918-4978-8c48-6e45b0987ee0": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "ebcdb664-00e7-4d76-8612-373a7ce38deb": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "8f5d95d7-e02d-446f-88e1-e96187bd1dbd": {
                "value": "backendexample3_dot_lan",
                "selected": 0
              },
              "1bf97d05-d8a3-4e84-a061-9bb0c8643ff8": {
                "value": "backendname",
                "selected": 0
              },
              "01efc324-c672-49f0-87eb-9a3f504957bc": {
                "value": "backendserver",
                "selected": 0
              }
            },
            "ssl_enabled": "0",
            "ssl_certificates": {
              "675d8e013920d": {
                "value": "dune60c585",
                "selected": 0
              },
              "66636c95283d1": {
                "value": "HPT630 2024",
                "selected": 0
              },
              "66c8f4b4d7cf6": {
                "value": "huub820g4india",
                "selected": 0
              },
              "66c9ed00ee302": {
                "value": "huubs9",
                "selected": 0
              },
              "66c9f245233d3": {
                "value": "ignas9",
                "selected": 0
              },
              "6779103ceca0b": {
                "value": "mm-frigate vpn",
                "selected": 0
              },
              "6676b0a67c9e8": {
                "value": "MXQ01",
                "selected": 0
              },
              "666616383dcf7": {
                "value": "parkodap 2024",
                "selected": 0
              },
              "6665996d6014f": {
                "value": "parkos22",
                "selected": 0
              },
              "6665753d5cfd4": {
                "value": "testhost",
                "selected": 0
              },
              "67a5e34d10086": {
                "value": "rene-laptop-1 2025 vpn certificate",
                "selected": 0
              },
              "67a5e0615d35b": {
                "value": "Rene Beemer 2025 laptop-1",
                "selected": 0
              },
              "666758edcb605": {
                "value": "stefan-van-bohemen-windows-11 2024",
                "selected": 0
              },
              "669102c4486f9": {
                "value": "tamara 2024",
                "selected": 0
              },
              "66646f9e9c0ea": {
                "value": "TM-1212",
                "selected": 0
              },
              "679dfa5a08e3a": {
                "value": "vpn.example.lan (ACME Client)",
                "selected": 0
              },
              "666354e39adc7": {
                "value": "VPN server 2024",
                "selected": 0
              },
              "663794b8efb60": {
                "value": "Web GUI TLS certificate",
                "selected": 0
              }
            },
            "ssl_default_certificate": {
              "": {
                "value": "None",
                "selected": 1
              },
              "675d8e013920d": {
                "value": "dune60c585",
                "selected": 0
              },
              "66636c95283d1": {
                "value": "HPT630 2024",
                "selected": 0
              },
              "66c8f4b4d7cf6": {
                "value": "huub820g4india",
                "selected": 0
              },
              "66c9ed00ee302": {
                "value": "huubs9",
                "selected": 0
              },
              "66c9f245233d3": {
                "value": "ignas9",
                "selected": 0
              },
              "6779103ceca0b": {
                "value": "mm-frigate vpn",
                "selected": 0
              },
              "6676b0a67c9e8": {
                "value": "MXQ01",
                "selected": 0
              },
              "666616383dcf7": {
                "value": "parkodap 2024",
                "selected": 0
              },
              "6665996d6014f": {
                "value": "parkos22",
                "selected": 0
              },
              "6665753d5cfd4": {
                "value": "testhost",
                "selected": 0
              },
              "67a5e34d10086": {
                "value": "rene-laptop-1 2025 vpn certificate",
                "selected": 0
              },
              "67a5e0615d35b": {
                "value": "Rene Beemer 2025 laptop-1",
                "selected": 0
              },
              "666758edcb605": {
                "value": "stefan-van-bohemen-windows-11 2024",
                "selected": 0
              },
              "669102c4486f9": {
                "value": "tamara 2024",
                "selected": 0
              },
              "66646f9e9c0ea": {
                "value": "TM-1212",
                "selected": 0
              },
              "679dfa5a08e3a": {
                "value": "vpn.example.lan (ACME Client)",
                "selected": 0
              },
              "666354e39adc7": {
                "value": "VPN server 2024",
                "selected": 0
              },
              "663794b8efb60": {
                "value": "Web GUI TLS certificate",
                "selected": 0
              }
            },
            "ssl_customOptions": "",
            "ssl_advancedEnabled": "0",
            "ssl_bindOptions": {
              "no-sslv3": {
                "value": "no-sslv3",
                "selected": 0
              },
              "no-tlsv10": {
                "value": "no-tlsv10",
                "selected": 0
              },
              "no-tlsv11": {
                "value": "no-tlsv11",
                "selected": 0
              },
              "no-tlsv12": {
                "value": "no-tlsv12",
                "selected": 0
              },
              "no-tlsv13": {
                "value": "no-tlsv13",
                "selected": 0
              },
              "no-tls-tickets": {
                "value": "no-tls-tickets",
                "selected": 0
              },
              "force-sslv3": {
                "value": "force-sslv3",
                "selected": 0
              },
              "force-tlsv10": {
                "value": "force-tlsv10",
                "selected": 0
              },
              "force-tlsv11": {
                "value": "force-tlsv11",
                "selected": 0
              },
              "force-tlsv12": {
                "value": "force-tlsv12",
                "selected": 0
              },
              "force-tlsv13": {
                "value": "force-tlsv13",
                "selected": 0
              },
              "prefer-client-ciphers": {
                "value": "prefer-client-ciphers",
                "selected": 1
              },
              "strict-sni": {
                "value": "strict-sni",
                "selected": 0
              }
            },
            "ssl_minVersion": {
              "": {
                "value": "None",
                "selected": 0
              },
              "SSLv3": {
                "value": "SSLv3",
                "selected": 0
              },
              "TLSv1.0": {
                "value": "TLSv1.0",
                "selected": 0
              },
              "TLSv1.1": {
                "value": "TLSv1.1",
                "selected": 0
              },
              "TLSv1.2": {
                "value": "TLSv1.2",
                "selected": 1
              },
              "TLSv1.3": {
                "value": "TLSv1.3",
                "selected": 0
              }
            },
            "ssl_maxVersion": {
              "": {
                "value": "None",
                "selected": 1
              },
              "SSLv3": {
                "value": "SSLv3",
                "selected": 0
              },
              "TLSv1.0": {
                "value": "TLSv1.0",
                "selected": 0
              },
              "TLSv1.1": {
                "value": "TLSv1.1",
                "selected": 0
              },
              "TLSv1.2": {
                "value": "TLSv1.2",
                "selected": 0
              },
              "TLSv1.3": {
                "value": "TLSv1.3",
                "selected": 0
              }
            },
            "ssl_cipherList": "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256",
            "ssl_cipherSuites": "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256",
            "ssl_hstsEnabled": "1",
            "ssl_hstsIncludeSubDomains": "0",
            "ssl_hstsPreload": "0",
            "ssl_hstsMaxAge": "15768000",
            "ssl_clientAuthEnabled": "0",
            "ssl_clientAuthVerify": {
              "": {
                "value": "None",
                "selected": 0
              },
              "none": {
                "value": "none",
                "selected": 0
              },
              "optional": {
                "value": "optional",
                "selected": 0
              },
              "required": {
                "value": "required",
                "selected": 1
              }
            },
            "ssl_clientAuthCAs": {
              "679dec55f3a64": {
                "value": "Example CA",
                "selected": 0
              },
              "679dfa5a00074": {
                "value": "ExampleCA Intermediate CA 2025 (ACME Client)",
                "selected": 0
              },
              "66635441877c1": {
                "value": "VPN 2024",
                "selected": 0
              }
            },
            "ssl_clientAuthCRLs": {
              "": {
                "value": "",
                "selected": 1
              }
            },
            "basicAuthEnabled": "0",
            "basicAuthUsers": [],
            "basicAuthGroups": [],
            "tuning_maxConnections": "",
            "tuning_timeoutClient": "",
            "tuning_timeoutHttpReq": "",
            "tuning_timeoutHttpKeepAlive": "",
            "linkedCpuAffinityRules": [],
            "tuning_shards": "",
            "logging_dontLogNull": "0",
            "logging_dontLogNormal": "0",
            "logging_logSeparateErrors": "0",
            "logging_detailedLog": "0",
            "logging_socketStats": "0",
            "stickiness_pattern": {
              "": {
                "value": "None",
                "selected": 1
              },
              "ipv4": {
                "value": "only store IPv4 addresses [default]",
                "selected": 0
              },
              "ipv6": {
                "value": "only store IPv6 addresses",
                "selected": 0
              },
              "integer": {
                "value": "store 32bit integers",
                "selected": 0
              },
              "string": {
                "value": "store substrings",
                "selected": 0
              },
              "binary": {
                "value": "store binary blocks",
                "selected": 0
              }
            },
            "stickiness_dataTypes": {
              "conn_cnt": {
                "value": "Connection count",
                "selected": 0
              },
              "conn_cur": {
                "value": "Current connections",
                "selected": 0
              },
              "conn_rate": {
                "value": "Connection rate",
                "selected": 0
              },
              "sess_cnt": {
                "value": "Session count",
                "selected": 0
              },
              "sess_rate": {
                "value": "Session rate",
                "selected": 0
              },
              "http_req_cnt": {
                "value": "HTTP request count",
                "selected": 0
              },
              "http_req_rate": {
                "value": "HTTP request rate",
                "selected": 0
              },
              "http_err_cnt": {
                "value": "HTTP error count",
                "selected": 0
              },
              "http_err_rate": {
                "value": "HTTP error rate",
                "selected": 0
              },
              "bytes_in_cnt": {
                "value": "Bytes in count (client to server)",
                "selected": 0
              },
              "bytes_in_rate": {
                "value": "Bytes in rate (client to server)",
                "selected": 0
              },
              "bytes_out_cnt": {
                "value": "Bytes out count (server to client)",
                "selected": 0
              },
              "bytes_out_rate": {
                "value": "Bytes out rate (server to client)",
                "selected": 0
              }
            },
            "stickiness_expire": "30m",
            "stickiness_size": "50k",
            "stickiness_counter": "1",
            "stickiness_counter_key": "src",
            "stickiness_length": "",
            "stickiness_connRatePeriod": "10s",
            "stickiness_sessRatePeriod": "10s",
            "stickiness_httpReqRatePeriod": "10s",
            "stickiness_httpErrRatePeriod": "10s",
            "stickiness_bytesInRatePeriod": "1m",
            "stickiness_bytesOutRatePeriod": "1m",
            "http2Enabled": "1",
            "http2Enabled_nontls": "0",
            "advertised_protocols": {
              "h2": {
                "value": "HTTP\/2",
                "selected": 1
              },
              "http11": {
                "value": "HTTP\/1.1",
                "selected": 1
              },
              "http10": {
                "value": "HTTP\/1.0",
                "selected": 0
              }
            },
            "forwardFor": "0",
            "prometheus_enabled": "0",
            "prometheus_path": "\/metrics",
            "connectionBehaviour": {
              "http-keep-alive": {
                "value": "http-keep-alive [default]",
                "selected": 1
              },
              "httpclose": {
                "value": "httpclose",
                "selected": 0
              },
              "http-server-close": {
                "value": "http-server-close",
                "selected": 0
              }
            },
            "customOptions": "",
            "linkedActions": {
              "4ad4fb72-d9cf-4b87-b5d3-434daffc46e3": {
                "value": "actionexample2_dot_lan",
                "selected": 1
              },
              "98f2b251-e2fb-4a10-9978-408c1f06eb27": {
                "value": "rulematchhostsample_example_org",
                "selected": 0
              },
              "e8959ab5-bba1-4bb3-8a36-ae7682073ac7": {
                "value": "rulename",
                "selected": 0
              },
              "66678189-587b-4359-bfad-a7536ec9d048": {
                "value": "actionexample2_dot_lan",
                "selected": 1
              },
              "e8ed7d90-be05-42f8-85e6-66db75c33c48": {
                "value": "actionexample2_dot_lan",
                "selected": 0
              },
              "1337bbee-852f-42ff-9d36-d94e986b079b": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "ca9faa1d-8a97-4fda-b187-17054dec9729": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "595ab0f2-9e85-4667-b530-e753453041b7": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "66368d90-d53d-48e0-8feb-5966e3930c87": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "f2fa3d36-3e70-42d4-9b36-acde30cd4e3d": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "9a1a3555-b323-4ef9-8865-f8e575140c0a": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "b62a09a7-aff8-4706-ba4c-7ad3d2c605a1": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "9ad1b1d1-29a0-44ea-8456-ea6c0249a940": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "6a021bb1-3a4d-4d03-8768-8ff12322ae58": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "11d7600e-527c-450b-a89e-bf7baf276aa0": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "a5ed968a-6f74-4c50-9625-ff61c74b0b58": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "7a78032a-02d6-4753-8819-4ae861e1abe2": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "85755a11-333a-492d-a892-28c037db523c": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "859c7c53-4300-4d04-b88b-ea568be036cd": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              },
              "de038241-4bdf-4f44-93ad-73fe954ceb31": {
                "value": "actionexample3_dot_lan",
                "selected": 0
              }
            },
            "linkedErrorfiles": []
          }
        }
        """
        return frontend_full

    def data_frontend_full_2(self):
        return r"""
        {"frontend": {"id": "676832e8a19d55.93978386", "enabled": "1", "name": "frontend", "description": "", "bind": {"192.168.1.1:443": {"value": "192.168.1.1:443", "selected": 1}}, "bindOptions": "", "mode": {"http": {"value": "HTTP / HTTPS (SSL offloading) [default]", "selected": 1}, "ssl": {"value": "SSL / HTTPS (TCP mode)", "selected": 0}, "tcp": {"value": "TCP", "selected": 0}}, "defaultBackend": {"": {"value": "None", "selected": 1}, "e853c9c6-b3b3-4640-ac88-000002d6702f": {"value": "acme_challenge_backend", "selected": 0}, "0e40ffff-b891-4700-b874-0000055adec0": {"value": "backend_media_dot_example_dot_com", "selected": 0}, "992de9f9-a555-47a7-afa6-0000016db57a": {"value": "docker-backend", "selected": 0}, "63572cd5-75af-49d7-ab55-0000054f67d9": {"value": "docker-backend-example", "selected": 0}, "85bc559e-5cb6-4b25-bfd4-000002506f48": {"value": "docker-node-js", "selected": 0}, "e0b9896a-4d7c-4747-bbbf-000005c8ff62": {"value": "webservice-pool", "selected": 0}}, "ssl_enabled": "1", "ssl_certificates": {"683f5b0376c1d": {"value": "media.example.com (ACME Client)", "selected": 0}, "6570b85e15754": {"value": "example.com (ACME Client)", "selected": 1}, "6710f81fd7fa1": {"value": "example2.com (ACME Client)", "selected": 1}, "f7fe081af001e": {"value": "Web GUI TLS certificate", "selected": 0}, "675efdc1100ff": {"value": "Web GUI TLS certificate", "selected": 0}, "675f006c21220": {"value": "Web GUI TLS certificate", "selected": 0}}, "ssl_default_certificate": {"": {"value": "None", "selected": 1}, "ff3f110376c00": {"value": "media.example.com (ACME Client)", "selected": 0}, "671058121a50f": {"value": "example.com (ACME Client)", "selected": 0}, "11707110fffae": {"value": "example2.com (ACME Client)", "selected": 0}, "6711fffa00e1e": {"value": "Web GUI TLS certificate", "selected": 0}, "115efdffa2007": {"value": "Web GUI TLS certificate", "selected": 0}, "11ff006caa5d3": {"value": "Web GUI TLS certificate", "selected": 0}}, "ssl_customOptions": "", "ssl_advancedEnabled": "0", "ssl_bindOptions": {"no-sslv3": {"value": "no-sslv3", "selected": 0}, "no-tlsv10": {"value": "no-tlsv10", "selected": 0}, "no-tlsv11": {"value": "no-tlsv11", "selected": 0}, "no-tlsv12": {"value": "no-tlsv12", "selected": 0}, "no-tlsv13": {"value": "no-tlsv13", "selected": 0}, "no-tls-tickets": {"value": "no-tls-tickets", "selected": 0}, "force-sslv3": {"value": "force-sslv3", "selected": 0}, "force-tlsv10": {"value": "force-tlsv10", "selected": 0}, "force-tlsv11": {"value": "force-tlsv11", "selected": 0}, "force-tlsv12": {"value": "force-tlsv12", "selected": 0}, "force-tlsv13": {"value": "force-tlsv13", "selected": 0}, "prefer-client-ciphers": {"value": "prefer-client-ciphers", "selected": 1}, "strict-sni": {"value": "strict-sni", "selected": 0}}, "ssl_minVersion": {"": {"value": "None", "selected": 0}, "SSLv3": {"value": "SSLv3", "selected": 0}, "TLSv1.0": {"value": "TLSv1.0", "selected": 0}, "TLSv1.1": {"value": "TLSv1.1", "selected": 0}, "TLSv1.2": {"value": "TLSv1.2", "selected": 1}, "TLSv1.3": {"value": "TLSv1.3", "selected": 0}}, "ssl_maxVersion": {"": {"value": "None", "selected": 1}, "SSLv3": {"value": "SSLv3", "selected": 0}, "TLSv1.0": {"value": "TLSv1.0", "selected": 0}, "TLSv1.1": {"value": "TLSv1.1", "selected": 0}, "TLSv1.2": {"value": "TLSv1.2", "selected": 0}, "TLSv1.3": {"value": "TLSv1.3", "selected": 0}}, "ssl_cipherList": "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256", "ssl_cipherSuites": "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256", "ssl_hstsEnabled": "1", "ssl_hstsIncludeSubDomains": "0", "ssl_hstsPreload": "0", "ssl_hstsMaxAge": "15768000", "ssl_clientAuthEnabled": "0", "ssl_clientAuthVerify": {"": {"value": "None", "selected": 0}, "none": {"value": "none", "selected": 0}, "optional": {"value": "optional", "selected": 0}, "required": {"value": "required", "selected": 1}}, "ssl_clientAuthCAs": {"00ff22ffd61af": {"value": "R10 (ACME Client)", "selected": 1}, "6771250409f25": {"value": "R11 (ACME Client)", "selected": 0}}, "ssl_clientAuthCRLs": [], "basicAuthEnabled": "0", "basicAuthUsers": [], "basicAuthGroups": [], "tuning_maxConnections": "", "tuning_timeoutClient": "", "tuning_timeoutHttpReq": "", "tuning_timeoutHttpKeepAlive": "", "linkedCpuAffinityRules": [], "tuning_shards": "", "logging_dontLogNull": "0", "logging_dontLogNormal": "0", "logging_logSeparateErrors": "0", "logging_detailedLog": "0", "logging_socketStats": "0", "stickiness_pattern": {"": {"value": "None", "selected": 1}, "ipv4": {"value": "only store IPv4 addresses [default]", "selected": 0}, "ipv6": {"value": "only store IPv6 addresses", "selected": 0}, "integer": {"value": "store 32bit integers", "selected": 0}, "string": {"value": "store substrings", "selected": 0}, "binary": {"value": "store binary blocks", "selected": 0}}, "stickiness_dataTypes": {"conn_cnt": {"value": "Connection count", "selected": 0}, "conn_cur": {"value": "Current connections", "selected": 0}, "conn_rate": {"value": "Connection rate", "selected": 0}, "sess_cnt": {"value": "Session count", "selected": 0}, "sess_rate": {"value": "Session rate", "selected": 0}, "http_req_cnt": {"value": "HTTP request count", "selected": 0}, "http_req_rate": {"value": "HTTP request rate", "selected": 0}, "http_err_cnt": {"value": "HTTP error count", "selected": 0}, "http_err_rate": {"value": "HTTP error rate", "selected": 0}, "bytes_in_cnt": {"value": "Bytes in count (client to server)", "selected": 0}, "bytes_in_rate": {"value": "Bytes in rate (client to server)", "selected": 0}, "bytes_out_cnt": {"value": "Bytes out count (server to client)", "selected": 0}, "bytes_out_rate": {"value": "Bytes out rate (server to client)", "selected": 0}}, "stickiness_expire": "30m", "stickiness_size": "50k", "stickiness_counter": "1", "stickiness_counter_key": "src", "stickiness_length": "", "stickiness_connRatePeriod": "10s", "stickiness_sessRatePeriod": "10s", "stickiness_httpReqRatePeriod": "10s", "stickiness_httpErrRatePeriod": "10s", "stickiness_bytesInRatePeriod": "1m", "stickiness_bytesOutRatePeriod": "1m", "http2Enabled": "1", "http2Enabled_nontls": "0", "advertised_protocols": {"h2": {"value": "HTTP/2", "selected": 1}, "http11": {"value": "HTTP/1.1", "selected": 1}, "http10": {"value": "HTTP/1.0", "selected": 0}}, "forwardFor": "0", "prometheus_enabled": "0", "prometheus_path": "/metrics", "connectionBehaviour": {"http-keep-alive": {"value": "http-keep-alive [default]", "selected": 1}, "httpclose": {"value": "httpclose", "selected": 0}, "http-server-close": {"value": "http-server-close", "selected": 0}}, "customOptions": "", "linkedActions": {"6c73bf9d-9837-48e6-b4a3-00000000000": {"value": "example", "selected": 1}, "d580e294-6d37-48d3-8f05-00000000000": {"value": "example2", "selected": 1}, "7c0a229b-faae-43c9-ad0a-00000000000": {"value": "server2", "selected": 1}, "b1280fae-c8af-415c-aff9-000000000000": {"value": "example3", "selected": 1}, "803f87ec-2e2e-4420-0000-000000000000": {"value": "redirect_acme_challenges", "selected": 0}, "94057719-0000-0000-0000-000000000000": {"value": "https_redirect", "selected": 0}, "a92e9ca3-0000-0000-0000-000000000000": {"value": "http headers upgrade", "selected": 0}, "00000000-0000-0000-0000-000000000000": {"value": "http  headers conn upgrade", "selected": 0}, "00000000-0000-0000-0000-000000000000": {"value": "http headers host", "selected": 0}, "00000008-0000-0000-0000-000000000000": {"value": "http headers set XRealip", "selected": 0}, "00000000-0000-0000-0000-000000000000": {"value": "http headers XForwardedFor", "selected": 0}, "00000000-0000-0000-0000-000000000000": {"value": "http headers XForwardedProto", "selected": 0}, "00000000-0000-0000-0000-000000000000": {"value": "action_media_dot_example_dot_com", "selected": 0}}, "linkedErrorfiles": []}}
        """

    def test_load_unload_2(self):
        frontend_full = self.data_frontend_full_2()
        #frontend_basic = self.data_frontend_basic_2()

        frontend_full_json = json.loads(frontend_full)
        full = Frontend.from_ui_dict(frontend_full_json) # type: Frontend
        #frontend_basic_json = json.loads(frontend_basic)
        #basic = FrontendResponseFrontend(**frontend_basic_json)
        self.assertEqual('frontend', full.name)
        # self.assertEqual("frontend', basic.frontend.name)
        # self.assertEqual(full.frontend.enabled, basic.frontend.enabled)
        # self.assertEqual(full.frontend.description, basic.frontend.description)
        # self.assertEqual(basic.frontend.bind, ",".join(str(v.value) for v in full.frontend.bind.values() if v.selected == 1))
        # self.assertEqual(basic.frontend.bind, full.frontend.get_frontend().bind)
        # self.assertEqual(basic.frontend.mode, full.frontend.get_frontend().mode)
        # self.assertEqual(basic.frontend.defaultBackend, full.frontend.get_frontend().defaultBackend)

        full_basic = full.to_simple_dict()
        # self.assertEqual(full_basic.__dict__, basic.frontend.__dict__)

        self.assertEqual(full.get_port(), '443')

    def data_action_basic_1(self):
        return '{"action":{"name":"1","description":"","testType":"if","linkedAcls":"","operator":"and","type":"use_backend","use_backend":"","use_server":"","http_request_auth":"","http_request_redirect":"","http_request_lua":"","http_request_use_service":"","http_request_add_header_name":"","http_request_add_header_content":"","http_request_set_header_name":"","http_request_set_header_content":"","http_request_del_header_name":"","http_request_replace_header_name":"","http_request_replace_header_regex":"","http_request_replace_value_name":"","http_request_replace_value_regex":"","http_request_set_path":"","http_request_set_var_scope":"txn","http_request_set_var_name":"","http_request_set_var_expr":"","http_response_lua":"","http_response_add_header_name":"","http_response_add_header_content":"","http_response_set_header_name":"","http_response_set_header_content":"","http_response_del_header_name":"","http_response_replace_header_name":"","http_response_replace_header_regex":"","http_response_replace_value_name":"","http_response_replace_value_regex":"","http_response_set_status_code":"","http_response_set_status_reason":"","http_response_set_var_scope":"txn","http_response_set_var_name":"","http_response_set_var_expr":"","monitor_fail_uri":"","tcp_request_content_lua":"","tcp_request_content_use_service":"","tcp_request_inspect_delay":"","tcp_response_content_lua":"","tcp_response_inspect_delay":"","custom":"","map_use_backend_file":"","map_use_backend_default":"","fcgi_pass_header":"","fcgi_set_param":""}}'

    def data_action_basic_2(self):
        return '{"action":{"name":"action","description":"actiondescription","testType":"if","linkedAcls":"","operator":"and","type":"use_backend","use_backend":"1bf97d05-d8a3-4e84-a061-9bb0c8643ff8","use_server":"","http_request_auth":"","http_request_redirect":"","http_request_lua":"","http_request_use_service":"","http_request_add_header_name":"","http_request_add_header_content":"","http_request_set_header_name":"","http_request_set_header_content":"","http_request_del_header_name":"","http_request_replace_header_name":"","http_request_replace_header_regex":"","http_request_replace_value_name":"","http_request_replace_value_regex":"","http_request_set_path":"","http_request_set_var_scope":"txn","http_request_set_var_name":"","http_request_set_var_expr":"","http_response_lua":"","http_response_add_header_name":"","http_response_add_header_content":"","http_response_set_header_name":"","http_response_set_header_content":"","http_response_del_header_name":"","http_response_replace_header_name":"","http_response_replace_header_regex":"","http_response_replace_value_name":"","http_response_replace_value_regex":"","http_response_set_status_code":"","http_response_set_status_reason":"","http_response_set_var_scope":"txn","http_response_set_var_name":"","http_response_set_var_expr":"","monitor_fail_uri":"","tcp_request_content_lua":"","tcp_request_content_use_service":"","tcp_request_inspect_delay":"","tcp_response_content_lua":"","tcp_response_inspect_delay":"","custom":"","map_use_backend_file":"","map_use_backend_default":"","fcgi_pass_header":"","fcgi_set_param":""}}'

    def data_action_full_1(self):
        return r'{"action":{"name":"1","description":"","testType":{"if":{"value":"IF [default]","selected":1},"unless":{"value":"UNLESS","selected":0}},"linkedAcls":{"497ed831-075f-4c01-8f90-d78362211837":{"value":"aclexample4_dot_lan","selected":0},"3dfed908-13bb-45ba-96dc-73085d3c6cf6":{"value":"aclexample4_dot_lan","selected":0},"9801984d-89d4-4a1f-ae68-3477e33a051d":{"value":"matchHostSample_example_org","selected":0},"dcc5c9e8-b388-477f-b9b5-f200e6ddeaed":{"value":"testacl","selected":0}},"operator":{"":{"value":"None","selected":0},"and":{"value":"AND [default]","selected":1},"or":{"value":"OR","selected":0}},"type":{"use_backend":{"value":"Use specified Backend Pool","selected":1},"use_server":{"value":"Override server in Backend Pool","selected":0},"map_use_backend":{"value":"Map domains to backend pools using a map file","selected":0},"fcgi_pass_header":{"value":"FastCGI pass-header","selected":0},"fcgi_set_param":{"value":"FastCGI set-param","selected":0},"http-request_allow":{"value":"http-request allow","selected":0},"http-request_deny":{"value":"http-request deny","selected":0},"http-request_tarpit":{"value":"http-request tarpit","selected":0},"http-request_auth":{"value":"http-request auth","selected":0},"http-request_redirect":{"value":"http-request redirect","selected":0},"http-request_lua":{"value":"http-request lua action","selected":0},"http-request_use-service":{"value":"http-request lua service","selected":0},"http-request_add-header":{"value":"http-request header add","selected":0},"http-request_set-header":{"value":"http-request header set","selected":0},"http-request_del-header":{"value":"http-request header delete","selected":0},"http-request_replace-header":{"value":"http-request header replace","selected":0},"http-request_replace-value":{"value":"http-request header replace value","selected":0},"http-request_set-path":{"value":"http-request set-path","selected":0},"http-request_set-var":{"value":"http-request set-var","selected":0},"http-response_allow":{"value":"http-response allow","selected":0},"http-response_deny":{"value":"http-response deny","selected":0},"http-response_lua":{"value":"http-response lua script","selected":0},"http-response_add-header":{"value":"http-response header add","selected":0},"http-response_set-header":{"value":"http-response header set","selected":0},"http-response_del-header":{"value":"http-response header delete","selected":0},"http-response_replace-header":{"value":"http-response header replace","selected":0},"http-response_replace-value":{"value":"http-response header replace value","selected":0},"http-response_set-status":{"value":"http-response set-status","selected":0},"http-response_set-var":{"value":"http-response set-var","selected":0},"monitor_fail":{"value":"monitor fail: report failure to a monitor request","selected":0},"tcp-request_connection_accept":{"value":"tcp-request connection accept","selected":0},"tcp-request_connection_reject":{"value":"tcp-request connection reject","selected":0},"tcp-request_content_accept":{"value":"tcp-request content accept","selected":0},"tcp-request_content_reject":{"value":"tcp-request content reject","selected":0},"tcp-request_content_lua":{"value":"tcp-request content lua script","selected":0},"tcp-request_content_use-service":{"value":"tcp-request content use-service","selected":0},"tcp-request_inspect-delay":{"value":"tcp-request inspect-delay","selected":0},"tcp-response_content_accept":{"value":"tcp-response content accept","selected":0},"tcp-response_content_close":{"value":"tcp-response content close","selected":0},"tcp-response_content_reject":{"value":"tcp-response content reject","selected":0},"tcp-response_content_lua":{"value":"tcp-response content lua script","selected":0},"tcp-response_inspect-delay":{"value":"tcp-response inspect-delay","selected":0},"custom":{"value":"Custom rule (option pass-through)","selected":0}},"use_backend":{"":{"value":"None","selected":1},"a004e352-8b9b-4cc3-b759-a5fbbab32544":{"value":"backendexample4_dot_lan","selected":0},"72ee45ad-1732-4901-ada7-ac5516c9a00b":{"value":"backendexample4_dot_lan","selected":0},"1bf97d05-d8a3-4e84-a061-9bb0c8643ff8":{"value":"backendname","selected":0},"01efc324-c672-49f0-87eb-9a3f504957bc":{"value":"backendserver","selected":0}},"use_server":{"":{"value":"None","selected":1},"1c650e12-298c-4774-9c13-0d8bf3515ed1":{"value":"realservername","selected":0},"6f0fe8b8-369e-4551-a15a-2288b5c50951":{"value":"realservername2","selected":0},"ec5027cd-cd29-4766-98ee-0c130912471c":{"value":"serverexample4_dot_lan","selected":0},"9066178a-38df-47e3-a582-2efb238c451e":{"value":"serverexample4_dot_lan","selected":0},"152d878b-c089-42bc-b8a1-00d93c578594":{"value":"testapi","selected":0},"66353d19-d9ea-4c9f-a817-4c73c3521ee9":{"value":"testname","selected":0}},"fcgi_pass_header":"","fcgi_set_param":"","http_request_auth":"","http_request_redirect":"","http_request_lua":"","http_request_use_service":"","http_request_add_header_name":"","http_request_add_header_content":"","http_request_set_header_name":"","http_request_set_header_content":"","http_request_del_header_name":"","http_request_replace_header_name":"","http_request_replace_header_regex":"","http_request_replace_value_name":"","http_request_replace_value_regex":"","http_request_set_path":"","http_request_set_var_scope":{"":{"value":"None","selected":0},"proc":{"value":"variable is shared with the whole process","selected":0},"sess":{"value":"variable is shared with the whole session","selected":0},"txn":{"value":"variable is shared with the transaction (request\\/response)","selected":1},"req":{"value":"variable is shared only during request processing","selected":0},"res":{"value":"variable is shared only during response processing","selected":0}},"http_request_set_var_name":"","http_request_set_var_expr":"","http_response_lua":"","http_response_add_header_name":"","http_response_add_header_content":"","http_response_set_header_name":"","http_response_set_header_content":"","http_response_del_header_name":"","http_response_replace_header_name":"","http_response_replace_header_regex":"","http_response_replace_value_name":"","http_response_replace_value_regex":"","http_response_set_status_code":"","http_response_set_status_reason":"","http_response_set_var_scope":{"":{"value":"None","selected":0},"proc":{"value":"variable is shared with the whole process","selected":0},"sess":{"value":"variable is shared with the whole session","selected":0},"txn":{"value":"variable is shared with the transaction (request\/response)","selected":1},"req":{"value":"variable is shared only during request processing","selected":0},"res":{"value":"variable is shared only during response processing","selected":0}},"http_response_set_var_name":"","http_response_set_var_expr":"","monitor_fail_uri":"","tcp_request_content_lua":"","tcp_request_content_use_service":"","tcp_request_inspect_delay":"","tcp_response_content_lua":"","tcp_response_inspect_delay":"","custom":"","useBackend":{"a004e352-8b9b-4cc3-b759-a5fbbab32544":{"value":"backendexample4_dot_lan","selected":0},"72ee45ad-1732-4901-ada7-ac5516c9a00b":{"value":"backendexample4_dot_lan","selected":0},"1bf97d05-d8a3-4e84-a061-9bb0c8643ff8":{"value":"backendname","selected":0},"01efc324-c672-49f0-87eb-9a3f504957bc":{"value":"backendserver","selected":0}},"useServer":{"1c650e12-298c-4774-9c13-0d8bf3515ed1":{"value":"realservername","selected":0},"6f0fe8b8-369e-4551-a15a-2288b5c50951":{"value":"realservername2","selected":0},"ec5027cd-cd29-4766-98ee-0c130912471c":{"value":"serverexample4_dot_lan","selected":0},"9066178a-38df-47e3-a582-2efb238c451e":{"value":"serverexample4_dot_lan","selected":0},"152d878b-c089-42bc-b8a1-00d93c578594":{"value":"testapi","selected":0},"66353d19-d9ea-4c9f-a817-4c73c3521ee9":{"value":"testname","selected":0}},"actionName":"","actionFind":"","actionValue":"","map_use_backend_file":{"":{"value":"None","selected":1}},"map_use_backend_default":{"":{"value":"None","selected":1},"a004e352-8b9b-4cc3-b759-a5fbbab32544":{"value":"backendexample4_dot_lan","selected":0},"72ee45ad-1732-4901-ada7-ac5516c9a00b":{"value":"backendexample4_dot_lan","selected":0},"1bf97d05-d8a3-4e84-a061-9bb0c8643ff8":{"value":"backendname","selected":0},"01efc324-c672-49f0-87eb-9a3f504957bc":{"value":"backendserver","selected":0}}}}'

    def test_load_result(self):
        data = {'result': 'saved'}
        obj = Result(**data)
        self.assertEqual('saved', obj.result)
