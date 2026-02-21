import json
from unittest import TestCase
from opnsense_api.pydantic.Acl import Acl


class TestPydanticAcl(TestCase):

    def data_acl_full_1(self):
        return """
{
  "acl": {
    "id": "68924593b08993.66592694",
    "name": "acl_sso_protected_frontends",
    "description": "All domains that require SSO",
    "expression": {
      "http_auth": {
        "value": "HTTP Basic Auth: username/password from client matches selected User/Group",
        "selected": 0
      },
      "hdr_beg": {
        "value": "Host starts with",
        "selected": 0
      },
      "hdr_end": {
        "value": "Host ends with",
        "selected": 0
      },
      "hdr": {
        "value": "Host matches",
        "selected": 1
      },
      "hdr_reg": {
        "value": "Host regex",
        "selected": 0
      },
      "hdr_sub": {
        "value": "Host contains",
        "selected": 0
      },
      "path_beg": {
        "value": "Path starts with",
        "selected": 0
      },
      "path_end": {
        "value": "Path ends with",
        "selected": 0
      },
      "path": {
        "value": "Path matches",
        "selected": 0
      },
      "path_reg": {
        "value": "Path regex",
        "selected": 0
      },
      "path_dir": {
        "value": "Path contains subdir",
        "selected": 0
      },
      "path_sub": {
        "value": "Path contains string",
        "selected": 0
      },
      "cust_hdr_beg": {
        "value": "HTTP Header starts with",
        "selected": 0
      },
      "cust_hdr_end": {
        "value": "HTTP Header ends with",
        "selected": 0
      },
      "cust_hdr": {
        "value": "HTTP Header matches",
        "selected": 0
      },
      "cust_hdr_reg": {
        "value": "HTTP Header regex",
        "selected": 0
      },
      "cust_hdr_sub": {
        "value": "HTTP Header contains",
        "selected": 0
      },
      "url_param": {
        "value": "URL parameter contains",
        "selected": 0
      },
      "ssl_c_verify": {
        "value": "SSL Client certificate is valid",
        "selected": 0
      },
      "ssl_c_verify_code": {
        "value": "SSL Client certificate verify error result",
        "selected": 0
      },
      "ssl_c_ca_commonname": {
        "value": "SSL Client certificate issued by CA common-name",
        "selected": 0
      },
      "ssl_hello_type": {
        "value": "SSL Hello Type",
        "selected": 0
      },
      "src": {
        "value": "Source IP matches specified IP",
        "selected": 0
      },
      "src_is_local": {
        "value": "Source IP is local",
        "selected": 0
      },
      "src_port": {
        "value": "Source IP: TCP source port",
        "selected": 0
      },
      "src_bytes_in_rate": {
        "value": "Source IP: incoming bytes rate",
        "selected": 0
      },
      "src_bytes_out_rate": {
        "value": "Source IP: outgoing bytes rate",
        "selected": 0
      },
      "src_kbytes_in": {
        "value": "Source IP: amount of data received (in kilobytes)",
        "selected": 0
      },
      "src_kbytes_out": {
        "value": "Source IP: amount of data sent (in kilobytes)",
        "selected": 0
      },
      "src_conn_cnt": {
        "value": "Source IP: cumulative number of connections",
        "selected": 0
      },
      "src_conn_cur": {
        "value": "Source IP: concurrent connections",
        "selected": 0
      },
      "src_conn_rate": {
        "value": "Source IP: connection rate",
        "selected": 0
      },
      "src_http_err_cnt": {
        "value": "Source IP: cumulative number of HTTP errors",
        "selected": 0
      },
      "src_http_err_rate": {
        "value": "Source IP: rate of HTTP errors",
        "selected": 0
      },
      "src_http_req_cnt": {
        "value": "Source IP: number of HTTP requests",
        "selected": 0
      },
      "src_http_req_rate": {
        "value": "Source IP: rate of HTTP requests",
        "selected": 0
      },
      "src_sess_cnt": {
        "value": "Source IP: cumulative number of sessions",
        "selected": 0
      },
      "src_sess_rate": {
        "value": "Source IP: session rate",
        "selected": 0
      },
      "nbsrv": {
        "value": "Minimum number of usable servers in backend",
        "selected": 0
      },
      "traffic_is_http": {
        "value": "Traffic is HTTP",
        "selected": 0
      },
      "traffic_is_ssl": {
        "value": "Traffic is SSL (TCP request content inspection)",
        "selected": 0
      },
      "ssl_fc": {
        "value": "Traffic is SSL (locally deciphered)",
        "selected": 0
      },
      "ssl_fc_sni": {
        "value": "SNI TLS extension matches (locally deciphered)",
        "selected": 0
      },
      "ssl_sni": {
        "value": "SNI TLS extension matches (TCP request content inspection)",
        "selected": 0
      },
      "ssl_sni_sub": {
        "value": "SNI TLS extension contains (TCP request content inspection)",
        "selected": 0
      },
      "ssl_sni_beg": {
        "value": "SNI TLS extension starts with (TCP request content inspection)",
        "selected": 0
      },
      "ssl_sni_end": {
        "value": "SNI TLS extension ends with (TCP request content inspection)",
        "selected": 0
      },
      "ssl_sni_reg": {
        "value": "SNI TLS extension regex (TCP request content inspection)",
        "selected": 0
      },
      "custom_acl": {
        "value": "Custom condition (option pass-through)",
        "selected": 0
      }
    },
    "negate": "0",
    "caseSensitive": "0",
    "hdr_beg": "",
    "hdr_end": "",
    "hdr": "",
    "hdr_reg": "",
    "hdr_sub": "",
    "path_beg": "",
    "path_end": "",
    "path": "",
    "path_reg": "",
    "path_dir": "",
    "path_sub": "",
    "cust_hdr_beg_name": "",
    "cust_hdr_beg": "",
    "cust_hdr_end_name": "",
    "cust_hdr_end": "",
    "cust_hdr_name": "",
    "cust_hdr": "",
    "cust_hdr_reg_name": "",
    "cust_hdr_reg": "",
    "cust_hdr_sub_name": "",
    "cust_hdr_sub": "",
    "url_param": "",
    "url_param_value": "",
    "ssl_c_verify_code": "",
    "ssl_c_ca_commonname": "",
    "ssl_hello_type": {
      "": {
        "value": "None",
        "selected": 0
      },
      "x0": {
        "value": "0 - no client hello",
        "selected": 0
      },
      "x1": {
        "value": "1 - client hello",
        "selected": 1
      },
      "x2": {
        "value": "2 - server hello",
        "selected": 0
      }
    },
    "src": "",
    "src_bytes_in_rate_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_bytes_in_rate": "",
    "src_bytes_out_rate_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_bytes_out_rate": "",
    "src_conn_cnt_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_conn_cnt": "",
    "src_conn_cur_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_conn_cur": "",
    "src_conn_rate_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_conn_rate": "",
    "src_http_err_cnt_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_http_err_cnt": "",
    "src_http_err_rate_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_http_err_rate": "",
    "src_http_req_cnt_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_http_req_cnt": "",
    "src_http_req_rate_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_http_req_rate": "",
    "src_kbytes_in_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_kbytes_in": "",
    "src_kbytes_out_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_kbytes_out": "",
    "src_port_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_port": "",
    "src_sess_cnt_comparison": {
      "": {
        "value": "None",
        "selected": 1
      },
      "gt": {
        "value": "greater than",
        "selected": 0
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_sess_cnt": "",
    "src_sess_rate_comparison": {
      "": {
        "value": "None",
        "selected": 0
      },
      "gt": {
        "value": "greater than",
        "selected": 1
      },
      "ge": {
        "value": "greater equal",
        "selected": 0
      },
      "eq": {
        "value": "equal",
        "selected": 0
      },
      "lt": {
        "value": "less than",
        "selected": 0
      },
      "le": {
        "value": "less equal",
        "selected": 0
      }
    },
    "src_sess_rate": "",
    "nbsrv": "",
    "nbsrv_backend": {
      "": {
        "value": "None",
        "selected": 1
      },
      "8b1b65a6-3297-4ebf-add7-180b372b9593": {
        "value": "some_name",
        "selected": 0
      },
      "67a2bcc8-eced-47ac-acbe-003b672e7f4c": {
        "value": "some_name",
        "selected": 0
      },
      "3dcbb6bd-1524-405c-b2f4-3b2f1dea0b22": {
        "value": "some_name",
        "selected": 0
      },
      "a042413c-e115-4d1e-9353-b967d46b12f3": {
        "value": "some_name",
        "selected": 0
      },
      "c6941c38-6bfd-48d7-ae63-635aa9c7ebac": {
        "value": "some_name",
        "selected": 0
      }
    },
    "ssl_fc_sni": "",
    "ssl_sni": "",
    "ssl_sni_sub": "",
    "ssl_sni_beg": "",
    "ssl_sni_end": "",
    "ssl_sni_reg": "",
    "custom_acl": "",
    "value": "",
    "urlparam": "",
    "queryBackend": {
      "": {
        "value": "None",
        "selected": 1
      },
      "8b1b65a6-3297-4ebf-add7-180b372b9593": {
        "value": "acme_challenge_backend",
        "selected": 0
      },
      "67a2bcc8-eced-47ac-acbe-003b672e7f4c": {
        "value": "some_name",
        "selected": 0
      },
      "3dcbb6bd-1524-405c-b2f4-3b2f1dea0b22": {
        "value": "some_name",
        "selected": 0
      },
      "a042413c-e115-4d1e-9353-b967d46b12f3": {
        "value": "some_name",
        "selected": 0
      },
      "c6941c38-6bfd-48d7-ae63-635aa9c7ebac": {
        "value": "some_name",
        "selected": 0
      }
    },
    "allowedUsers": [],
    "allowedGroups": []
  }
}
"""

    def test_acl_load(self):
        acl_full = self.data_acl_full_1()
        acl_full_json = json.loads(acl_full)
        acl = Acl.from_ui_dict(acl_full_json)
        response_acl = acl.to_simple_dict()
        self.assertEqual('acl_sso_protected_frontends', response_acl['acl']['name'])
