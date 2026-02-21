from opnsense_api.api.acmeclient_accounts_client import AcmeclientAccountsClient
from opnsense_api.api.acmeclient_validations_client import AcmeclientValidationsClient
from opnsense_api.api.auth_group_client import AuthGroup
from opnsense_api.api.auth_user_client import AuthUser
from opnsense_api.api.firewall_alias_client import FirewallAliasClient
from opnsense_api.api.firewall_category_client import FirewallCategoryClient
from opnsense_api.api.firewall_filter_client import FirewallFilterClient
from opnsense_api.api.firewall_snat_client import FirewallSnatClient
from opnsense_api.api.firewall_one_to_one_client import FirewallOneToOneClient
from opnsense_api.api.firewall_dnat_client import FirewallDnatClient
from opnsense_api.api.haproxy import Haproxy
from opnsense_api.api.haproxy_export_client import HaproxyExportClient
from opnsense_api.api.haproxy_settings_client import HaproxySettingsClient
from opnsense_api.api.interfaces_overview_client import InterfacesOverviewClient
from opnsense_api.api.interfaces_vlan_client import InterfacesVlanClient
from opnsense_api.api.kea_dhcpv4_client import KeaDhcpv4Client
from opnsense_api.api.unbound_client import UnboundClient
from opnsense_api.api.trust import Trust
from opnsense_api.base_client import BaseClient
from opnsense_api.api.core_backup_client import CoreBackupClient
from opnsense_api.api.core_firmware_client import CoreFirmwareClient


class Client(UnboundClient, KeaDhcpv4Client, InterfacesVlanClient, InterfacesOverviewClient, FirewallDnatClient, FirewallOneToOneClient, FirewallSnatClient, FirewallFilterClient, FirewallCategoryClient, FirewallAliasClient, Haproxy, AuthGroup, AuthUser, CoreBackupClient, CoreFirmwareClient, Trust, HaproxyExportClient, HaproxySettingsClient,
             AcmeclientAccountsClient, AcmeclientValidationsClient, BaseClient):

    def state(self) -> 'StateManager':
        """
        Get a StateManager for desired state configuration.

        The StateManager provides a declarative interface to define
        desired network state and compare/apply changes to OPNsense.

        Example:
            >>> state = client.state()
            >>> state.dns_host(hostname='server1', domain='lan', ip='192.168.1.100')
            >>> changes = state.plan()
            >>> state.apply(auto_approve=True)

        Returns:
            StateManager instance bound to this client
        """
        from opnsense_api.state import StateManager
        return StateManager(self)
