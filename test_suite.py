import unittest
from tests.test_firewall_filter import TestFirewallFilter
from tests.test_firewall_snat import TestFirewallSnat
from tests.test_firewall_one_to_one import TestFirewallOneToOne
from tests.test_helper import TestHelper
from tests.test_rule_model_issues import TestRuleModelIssues
from tests.test_pydantic_acl import TestPydanticAcl
from tests.test_pydantic_acmeclient import TestPydanticAcmeClient
from tests.test_pydantic_action import TestPydanticAction
from tests.test_pydantic_action_order import TestPydanticActionOrder
from tests.test_pydantic_alias import TestPydanticAlias
from tests.test_pydantic_auth import TestPydanticAuth
from tests.test_pydantic_backend import TestPydanticBackend
from tests.test_pydantic_cert import TestPydanticCert
from tests.test_pydantic_frontend import TestPydanticFrontend
from tests.test_pydantic_server import TestPydanticServer
from tests.test_interface_overview import TestInterfaceOverview, TestInterfaceExport
from tests.test_model_serialization import (
    TestVlanSerialization, TestRuleSerialization, TestSNATRuleSerialization,
    TestOneToOneRuleSerialization, TestRoundTripSerialization
)
from tests.test_kea_dhcpv4 import TestSubnet4, TestReservation, TestPeer
from tests.test_core_backup import TestCoreBackup
from tests.test_unbound import (
    TestAcl, TestHost, TestDot, TestAlias, TestBlocklist,
    TestGeneral, TestAdvanced, TestAcls, TestForwarding, TestUnboundSettings
)


suiteList = []
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticAcl))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestHelper))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticAction))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticBackend))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticFrontend))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticServer))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticAcmeClient))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticCert))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticAlias))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticActionOrder))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPydanticAuth))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestFirewallFilter))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestFirewallSnat))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestFirewallOneToOne))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestRuleModelIssues))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestInterfaceOverview))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestInterfaceExport))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestVlanSerialization))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestRuleSerialization))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestSNATRuleSerialization))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestOneToOneRuleSerialization))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestRoundTripSerialization))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestSubnet4))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestReservation))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestPeer))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestAcl))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestHost))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestDot))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestAlias))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestBlocklist))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestGeneral))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestAdvanced))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestAcls))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestForwarding))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestUnboundSettings))
suiteList.append(unittest.TestLoader().loadTestsFromTestCase(TestCoreBackup))


comboSuite = unittest.TestSuite(suiteList)
unittest.TextTestRunner(verbosity=0).run(comboSuite)
