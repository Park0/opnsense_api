#!/usr/bin/env python3
"""
Example: Unbound DNS API usage

Demonstrates managing Unbound DNS settings, host overrides, ACLs,
DNS-over-TLS forwarding, and blocklists.
"""
from opnsense_api.client import Client
from opnsense_api.pydantic.Unbound import (
    Acl, Host, Alias, Dot, Blocklist, General
)

# Initialize client
client = Client(
    base_url='https://your-opnsense.local/api',
    api_key='your-api-key',
    api_secret='your-api-secret',
    verify_cert=False
)

# ============================================================
# Host Overrides (DNS A/AAAA/MX/TXT records)
# ============================================================

# Create a host override (A record)
host = Host(
    enabled=True,
    hostname="server1",
    domain="example.lan",
    server="192.168.1.100",
    description="Web Server"
)
result = client.unbound_add_host_override(host)
host_uuid = result.uuid
print(f"Created host override: {host_uuid}")

# List all host overrides
hosts = client.unbound_search_host_override()
for h in hosts.rows:
    print(f"  {h.hostname}.{h.domain} -> {h.server}")

# Update host override
host = client.unbound_get_host_override(host_uuid)
host.description = "Updated Web Server"
client.unbound_set_host_override(host_uuid, host)

# Toggle enable/disable
client.unbound_toggle_host_override(host_uuid, enabled=False)

# Delete host override
# client.unbound_del_host_override(host_uuid)

# ============================================================
# Host Aliases (CNAME-like aliases pointing to host overrides)
# ============================================================

# Create a host alias
alias = Alias(
    enabled=True,
    host=host_uuid,  # UUID of the host override to alias
    hostname="www",
    domain="example.lan",
    description="WWW alias"
)
result = client.unbound_add_host_alias(alias)
print(f"Created host alias: {result.uuid}")

# List all host aliases
aliases = client.unbound_search_host_alias()
for a in aliases.rows:
    print(f"  {a.hostname}.{a.domain} -> {a.host}")

# ============================================================
# Access Control Lists (ACLs)
# ============================================================

# Create an ACL
acl = Acl(
    enabled=True,
    name="Internal Networks",
    action=Acl.AclsAclActionEnum.ALLOW,
    networks=["10.0.0.0/8", "192.168.0.0/16"],
    description="Allow internal networks"
)
result = client.unbound_add_acl(acl)
print(f"Created ACL: {result.uuid}")

# List all ACLs
acls = client.unbound_search_acl()
for a in acls.rows:
    print(f"  {a.name}: {a.action} ({a.networks})")

# ============================================================
# DNS-over-TLS / Forwarding
# ============================================================

# Create a DoT forward to Cloudflare
dot = Dot(
    enabled=True,
    type=Dot.DotsDotTypeEnum.DOT,
    server="1.1.1.1",
    port=853,
    verify="cloudflare-dns.com",
    description="Cloudflare DoT"
)
result = client.unbound_add_forward(dot)
print(f"Created DoT forward: {result.uuid}")

# Create a plain DNS forward
forward = Dot(
    enabled=True,
    type=Dot.DotsDotTypeEnum.FORWARD,
    domain="internal.corp",  # Only forward queries for this domain
    server="10.0.0.1",
    description="Internal DNS forward"
)
result = client.unbound_add_forward(forward)
print(f"Created DNS forward: {result.uuid}")

# List all forwards
forwards = client.unbound_search_forward()
for f in forwards.rows:
    print(f"  {f.domain or '*'}: {f.server} ({f.type})")

# ============================================================
# DNS Blocklists (DNSBL)
# ============================================================

# Create a blocklist policy
blocklist = Blocklist(
    enabled=True,
    type=[
        Blocklist.DnsblBlocklistTypeEnum.AG,  # AdGuard List
        Blocklist.DnsblBlocklistTypeEnum.SB   # Steven Black List
    ],
    source_nets=["192.168.1.0/24"],  # Apply only to this network
    description="Ad blocking for LAN"
)
result = client.unbound_add_dnsbl(blocklist)
print(f"Created blocklist: {result.uuid}")

# Update blocklists (download latest)
client.unbound_update_blocklist()
print("Blocklists updated")

# ============================================================
# General Settings
# ============================================================

# Get current settings (returns UnboundSettings object)
settings = client.unbound_get()
print(f"Unbound enabled: {settings.general.enabled}")
print(f"DNS port: {settings.general.port}")
print(f"DNSSEC: {settings.general.dnssec}")

# Get configured nameservers (returns List[str])
nameservers = client.unbound_get_nameservers()
print(f"Nameservers: {nameservers}")

# Modify settings using UnboundSettings model
from opnsense_api.pydantic.Unbound import UnboundSettings, General

new_settings = UnboundSettings(
    general=General(
        enabled=True,
        port=53,
        dnssec=True
    )
)
client.unbound_set(new_settings)
