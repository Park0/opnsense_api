# opnsense-api

Typed Python bindings for the [OPNsense REST API](https://docs.opnsense.org/development/api.html) with Pydantic model validation.

## Installation

```bash
pip install opnsense-api2
```

With Authentik SSO support:

```bash
pip install opnsense-api2[authentik]
```

## Quick start

```python
from opnsense_api.client import Client

client = Client(
    api_key="your-api-key",
    api_secret="your-api-secret",
    base_url="https://opnsense.local/api",
    verify_cert="/path/to/root-ca.pem",
)

# List all firewall aliases
aliases = client.firewall_alias_search()

# Add a DNS host override
client.unbound_add_host_override(hostname="server1", domain="lan", server="192.168.1.100")

# Get firmware status
info = client.firmware_info()
```

## Desired state management

Declare your desired OPNsense configuration in Python or YAML and let the state manager figure out the diff:

```python
state = client.state()

state.dns_host(hostname="server1", domain="lan", ip="192.168.1.100")
state.firewall_alias(name="trusted_hosts", type="host", content=["10.0.0.1", "10.0.0.2"])
state.firewall_rule(interface="lan", source_net="trusted_hosts", destination_port="443", action="pass")

changes = state.plan()   # preview changes
state.apply()            # apply after confirmation
```

Or from a YAML file:

```python
state = client.state()
state.load_yaml("desired_state.yaml")
state.apply(auto_approve=True)
```

## Supported APIs

| Area | Operations |
|------|-----------|
| **Firewall** | Filter rules, aliases, categories, DNAT (port forward), SNAT, 1:1 NAT |
| **HAProxy** | Servers, backends, frontends, ACLs, actions, settings, export, service control |
| **Unbound DNS** | Host overrides, domain overrides, settings |
| **Kea DHCPv4** | Subnets, reservations, settings |
| **Trust** | CAs, certificates, CRLs |
| **ACME Client** | Accounts, certificates, validations |
| **Interfaces** | Overview, VLANs |
| **Auth** | Users, groups |
| **Core** | Config backup/export, firmware info |
| **Authentik SSO** | HAProxy + Authentik integration |

## CLI

The `opn` command provides quick access to common operations:

```bash
# Interactive config setup
opn config

# Create an HAProxy reverse proxy rule
opn haproxy --domain example.com --ip 10.0.0.5 --port 8080 \
    --frontend MAIN-HTTPS --ssl-provider "Letsencrypt"

# With Authentik SSO
opn haproxy --domain app.example.com --ip 10.0.0.5 --port 8080 \
    --frontend MAIN-HTTPS --ssl-provider "Letsencrypt" --sso authentik

# Toggle SSO on a domain
opn sso --domain app.example.com --enable
opn sso --domain app.example.com --disable
```

Configuration is resolved in order: `config.yml` < environment variables < CLI flags.

## Development

```bash
pip install -r requirements.txt
python3 -m unittest test_suite.py
```

Inspired by [pyopnsense](https://github.com/mtreinish/pyopnsense).
