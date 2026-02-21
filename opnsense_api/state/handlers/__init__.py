"""
Entity handlers for state management.
"""
from opnsense_api.state.handlers.base_handler import EntityHandler
from opnsense_api.state.handlers.dns_host_handler import DnsHostHandler
from opnsense_api.state.handlers.dhcp_reservation_handler import DhcpReservationHandler
from opnsense_api.state.handlers.firewall_alias_handler import FirewallAliasHandler
from opnsense_api.state.handlers.firewall_rule_handler import FirewallRuleHandler

__all__ = [
    'EntityHandler',
    'DnsHostHandler',
    'DhcpReservationHandler',
    'FirewallAliasHandler',
    'FirewallRuleHandler',
]
