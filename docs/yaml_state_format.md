# YAML State Configuration Format

This document describes the YAML format used by PySense's state management system for declaring desired OPNsense configuration.

## Overview

The state management system allows you to define your desired OPNsense configuration in a declarative YAML file. You can then compare this desired state against the actual state in OPNsense and apply changes automatically.

## Quick Start

```python
from opnsense_api.client import Client

client = Client(base_url='https://opnsense.local/api', api_key='...', api_secret='...')
state = client.state()

# Load desired state from YAML
state.load_yaml('my_config.yaml')

# Compare with actual state
changes = state.plan()
print(state.format_plan(changes))

# Apply changes
state.apply(auto_approve=True)
```

## YAML Structure

The YAML file contains multiple sections for different entity types:

```yaml
dns_hosts:              # DNS host overrides (Unbound)
dhcp_reservations:      # Static DHCP leases (Kea)
firewall_aliases:       # Named IP/network/port groups
firewall_rules:         # Firewall filter rules
interfaces:             # Network interfaces (compare-only)
vlans:                  # VLAN configurations
snat_rules:             # Source NAT (Outbound NAT) rules
one_to_one_nat_rules:   # 1:1 NAT (bidirectional NAT) rules
dnat_rules:             # DNAT / Port Forward rules
```

All sections are optional. You can include only the sections relevant to your configuration.

### UUID Support

All entity types support an optional `uuid` field. When exporting state, UUIDs are included automatically. When importing:

- If `uuid` is provided, the entity is matched by UUID first (exact match)
- If no UUID match, falls back to primary key matching (hostname, name, etc.)
- Using UUIDs ensures reliable matching even if primary keys change

```yaml
dns_hosts:
  - uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567890  # Optional: exact match by UUID
    hostname: server1
    domain: lan
    ip: 192.168.1.100
```

---

## DNS Host Overrides

Maps hostnames to IP addresses for local DNS resolution. These override external DNS for the specified hostnames.

### Schema

```yaml
dns_hosts:
  - uuid: <string>           # Optional: UUID for exact matching
    hostname: <string>       # Required: hostname without domain
    domain: <string>         # Required: domain name
    ip: <string>             # Required: IP address (IPv4 or IPv6)
    description: <string>    # Optional: human-readable description
```

### Example

```yaml
dns_hosts:
  - uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567890
    hostname: nas
    domain: lan
    ip: 192.168.1.10
    description: Network storage server

  - hostname: proxmox
    domain: lan
    ip: 192.168.1.20
    description: Virtualization host

  - hostname: printer
    domain: home.arpa
    ip: 192.168.1.30
```

### Notes

- The full FQDN will be `{hostname}.{domain}` (e.g., `nas.lan`)
- Common domains: `lan`, `local`, `home.arpa`, `internal`
- Supports both IPv4 and IPv6 addresses

---

## DHCP Reservations

Static IP assignments based on MAC address. The DHCP server will always assign the same IP to the specified MAC.

### Schema

```yaml
dhcp_reservations:
  - uuid: <string>           # Optional: UUID for exact matching
    mac: <string>            # Required: MAC address
    ip: <string>             # Required: reserved IP address
    hostname: <string>       # Optional: hostname to assign via DHCP
    description: <string>    # Optional: human-readable description
```

### Example

```yaml
dhcp_reservations:
  - mac: aa:bb:cc:dd:ee:01
    ip: 192.168.1.10
    hostname: nas
    description: Network storage server

  - mac: AA:BB:CC:DD:EE:02
    ip: 192.168.1.20
    hostname: proxmox

  - mac: aa-bb-cc-dd-ee-03
    ip: 192.168.1.30
    hostname: printer
```

### Notes

- MAC address formats supported: `aa:bb:cc:dd:ee:ff`, `AA:BB:CC:DD:EE:FF`, `aa-bb-cc-dd-ee-ff`
- IP must be within the DHCP pool's subnet
- Hostname is optional but recommended for easier identification

---

## Firewall Aliases

Named groups of IPs, networks, or ports for use in firewall rules. Using aliases makes rules more readable and easier to maintain.

### Schema

```yaml
firewall_aliases:
  - uuid: <string>           # Optional: UUID for exact matching
    name: <string>           # Required: unique alias name (alphanumeric + underscore)
    type: <string>           # Required: alias type (see types below)
    content:                 # Required: list of items
      - <string>
    description: <string>    # Optional: human-readable description
    enabled: <boolean>       # Optional: default true
```

### Alias Types

| Type | Description | Content Examples |
|------|-------------|------------------|
| `host` | Individual IP addresses | `192.168.1.1`, `10.0.0.5` |
| `network` | CIDR network ranges | `192.168.1.0/24`, `10.0.0.0/8` |
| `port` | TCP/UDP port numbers | `80`, `443`, `8080-8090` |
| `url` | IP list fetched from URL | `https://example.com/blocklist.txt` |
| `urltable` | URL table for large lists | `https://example.com/large-list.txt` |
| `geoip` | Geographic IP blocks | Country codes |
| `asn` | Autonomous System Numbers | `AS12345` |
| `dynipv6host` | Dynamic IPv6 host | IPv6 prefix |
| `authgroup` | Authentication group | Group names |

### Example

```yaml
firewall_aliases:
  - name: trusted_networks
    type: network
    content:
      - 192.168.1.0/24
      - 192.168.2.0/24
      - 10.0.0.0/8
    description: Internal trusted networks

  - name: management_hosts
    type: host
    content:
      - 192.168.1.10
      - 192.168.1.20
    description: Servers that can be managed

  - name: web_ports
    type: port
    content:
      - "80"
      - "443"
      - "8080-8090"
    description: Common web ports

  - name: blocked_countries
    type: geoip
    content:
      - CN
      - RU
      - KP
    description: Blocked geographic regions
```

### Notes

- Alias names must be unique and contain only alphanumeric characters and underscores
- Port numbers should be quoted to ensure they're treated as strings
- Port ranges use dash notation: `8080-8090`
- Internal and external aliases (system-managed) are skipped during export

---

## Firewall Rules

Traffic filtering rules. **Order matters** - first matching rule wins!

### Schema

```yaml
firewall_rules:
  - uuid: <string>           # Optional: UUID for exact matching
    action: <string>         # Required: pass, block, reject
    interface:               # Optional: list of interface names
      - <string>
    source: <string>         # Optional: source address (default: any)
    destination: <string>    # Optional: destination address (default: any)
    protocol: <string>       # Optional: protocol (default: any)
    destination_port: <string>  # Optional: destination port(s)
    description: <string>    # Recommended: unique description for matching
    enabled: <boolean>       # Optional: default true
    log: <boolean>           # Optional: default false
```

### Actions

| Action | Description |
|--------|-------------|
| `pass` | Allow the traffic |
| `block` | Silently drop the traffic |
| `reject` | Drop with ICMP unreachable response |

### Protocols

| Protocol | Description |
|----------|-------------|
| `any` | Any protocol (default) |
| `tcp` | TCP only |
| `udp` | UDP only |
| `tcp/udp` | Both TCP and UDP |
| `icmp` | ICMP (ping, etc.) |
| `esp` | IPsec ESP |
| `ah` | IPsec AH |
| `gre` | GRE tunneling |

### Source/Destination Values

- `any` - Any address
- IP address: `192.168.1.1`
- CIDR notation: `192.168.1.0/24`
- Alias name: `trusted_networks`
- Special values: `(self)` for firewall itself

### Example

```yaml
firewall_rules:
  # Allow HTTPS from trusted networks
  - action: pass
    interface:
      - lan
    source: trusted_networks
    destination: any
    protocol: tcp
    destination_port: "443"
    description: Allow HTTPS from trusted networks

  # Allow SSH to management hosts only
  - action: pass
    interface:
      - lan
    source: any
    destination: management_hosts
    protocol: tcp
    destination_port: "22"
    description: Allow SSH to management hosts

  # Allow DNS
  - action: pass
    interface:
      - lan
    source: any
    destination: any
    protocol: udp
    destination_port: "53"
    description: Allow DNS queries

  # Allow multiple ports
  - action: pass
    interface:
      - lan
    destination_port: "80,443,8080"
    description: Allow web traffic

  # Block all inbound WAN traffic (log it)
  - action: block
    interface:
      - wan
    source: any
    destination: any
    description: Block all inbound WAN traffic
    log: true

  # Disabled rule (for reference)
  - action: pass
    interface:
      - lan
    description: Temporarily disabled rule
    enabled: false
```

### Notes

- **Always provide a unique `description`** for rules you want to manage - this is how rules are matched
- Rules without descriptions may not match reliably during updates
- Port numbers should be quoted: `"443"` not `443`
- Multiple ports: `"80,443,8080"` or use a port alias
- Port ranges: `"1024-65535"`
- Interface names are lowercase: `lan`, `wan`, `opt1`, `opt2`

---

## Interfaces (Compare-Only)

Network interface configuration. **These are compare-only** - changes cannot be applied automatically and must be configured manually through the OPNsense web UI.

### Schema

```yaml
interfaces:
  - identifier: <string>     # Required: interface identifier (lan, wan, opt1)
    description: <string>    # Optional: display name (LAN, WAN, DMZ)
    device: <string>         # Optional: physical device (vmx0, em0, igb0)
    enabled: <boolean>       # Optional: default true
    link_type: <string>      # Optional: static, dhcp, pppoe, etc.
    addr4: <string>          # Optional: IPv4 address with CIDR
    addr6: <string>          # Optional: IPv6 address with prefix
    mtu: <integer>           # Optional: maximum transmission unit
```

### Link Types

| Type | Description |
|------|-------------|
| `static` | Static IP configuration |
| `dhcp` | DHCP client |
| `pppoe` | PPPoE (DSL connections) |
| `pptp` | PPTP VPN |
| `l2tp` | L2TP VPN |
| `none` | No IP configuration |

### Example

```yaml
interfaces:
  - identifier: wan
    description: WAN
    device: vmx0
    enabled: true
    link_type: dhcp

  - identifier: lan
    description: LAN
    device: vmx1
    enabled: true
    link_type: static
    addr4: 192.168.1.1/24
    mtu: 1500

  - identifier: opt1
    description: DMZ
    device: vmx2
    enabled: true
    link_type: static
    addr4: 10.0.0.1/24
```

### Notes

- **Compare-only**: Interface changes are shown in the plan but must be applied manually
- The plan will show `[MANUAL]` prefix for interface changes
- Configure interfaces through: Interfaces > [interface name] in OPNsense web UI
- Use `identifier` for matching (lan, wan, opt1, opt2, etc.)

---

## VLANs

VLAN interface configuration. VLANs **can be fully managed** via API (create, update, delete).

### Schema

```yaml
vlans:
  - uuid: <string>           # Optional: UUID for exact matching
    interface: <string>      # Required: parent interface device (vmx0, em0)
    tag: <integer>           # Required: VLAN tag (1-4094)
    description: <string>    # Optional: VLAN description
    pcp: <integer>           # Optional: Priority Code Point (0-7, default 0)
    proto: <string>          # Optional: 802.1q or 802.1ad (default 802.1q)
    vlanif: <string>         # Read-only: resulting VLAN interface name
```

### VLAN Protocols

| Protocol | Description |
|----------|-------------|
| `802.1q` | Standard VLAN tagging (default) |
| `802.1ad` | Q-in-Q (stacked VLANs) |

### Example

```yaml
vlans:
  - interface: vmx0
    tag: 100
    description: Management VLAN
    pcp: 0
    proto: 802.1q

  - interface: vmx0
    tag: 200
    description: Guest VLAN

  - interface: vmx1
    tag: 300
    description: IoT VLAN
    pcp: 2
```

### Notes

- **Fully managed**: VLANs can be created, updated, and deleted via API
- Parent `interface` must be the device name (e.g., `vmx0`), not the identifier (e.g., `wan`)
- `vlanif` is read-only and shows the resulting interface name (e.g., `vmx0_vlan100`)
- After VLAN creation, assign it to an OPNsense interface through the web UI
- VLAN changes are automatically applied via `vlan_reconfigure()`

---

## Source NAT Rules (Outbound NAT)

Source NAT (SNAT) rules control how outgoing traffic is translated/masqueraded. **Fully managed** via API.

### Schema

```yaml
snat_rules:
  - uuid: <string>           # Optional: UUID for exact matching
    interface: <string>      # Required: outbound interface (wan)
    source_net: <string>     # Optional: source network/alias (default: any)
    destination_net: <string> # Optional: destination network/alias (default: any)
    target: <string>         # Optional: NAT target (default: wanip)
    enabled: <boolean>       # Optional: default true
    nonat: <boolean>         # Optional: disable NAT for this match (default: false)
    protocol: <string>       # Optional: any, tcp, udp, etc.
    source_port: <string>    # Optional: source port filter
    destination_port: <string> # Optional: destination port filter
    target_port: <string>    # Optional: target port translation
    ipprotocol: <string>     # Optional: inet (IPv4) or inet6 (IPv6)
    sequence: <integer>      # Optional: rule order (1-99999)
    log: <boolean>           # Optional: log matches (default: false)
    description: <string>    # Recommended: for rule matching
```

### Target Values

| Target | Description |
|--------|-------------|
| `wanip` | Use WAN interface IP (default) |
| `any` | No translation (use with nonat) |
| `<IP address>` | Specific IP for translation |
| `<alias>` | Use alias for IP pool |

### Example

```yaml
snat_rules:
  # Standard outbound NAT for LAN
  - interface: wan
    source_net: 192.168.1.0/24
    target: wanip
    description: LAN outbound NAT

  # No NAT for VPN traffic
  - interface: wan
    source_net: 10.0.0.0/8
    destination_net: 10.0.0.0/8
    nonat: true
    description: Skip NAT for VPN

  # Port forwarding with translation
  - interface: wan
    source_net: 192.168.1.100
    protocol: tcp
    destination_port: "80"
    target: 203.0.113.10
    target_port: "8080"
    description: Web server outbound
```

---

## 1:1 NAT Rules (One-to-One NAT)

1:1 NAT rules map external IPs to internal hosts bidirectionally. **Fully managed** via API.

### Schema

```yaml
one_to_one_nat_rules:
  - uuid: <string>           # Optional: UUID for exact matching
    external: <string>       # Required: external IP address
    source_net: <string>     # Required: internal host/network
    interface: <string>      # Optional: external interface (default: wan)
    enabled: <boolean>       # Optional: default true
    nat_type: <string>       # Optional: binat or nat (default: binat)
    destination_net: <string> # Optional: destination filter (default: any)
    natreflection: <string>  # Optional: '', 'enable', 'disable'
    sequence: <integer>      # Optional: rule order (1-99999)
    log: <boolean>           # Optional: log matches (default: false)
    description: <string>    # Recommended: for rule matching
```

### NAT Types

| Type | Description |
|------|-------------|
| `binat` | Bidirectional NAT (default) - maps both directions |
| `nat` | Unidirectional NAT - inbound only |

### NAT Reflection

| Value | Description |
|-------|-------------|
| `''` (empty) | Use system default |
| `enable` | Enable hairpin NAT for this rule |
| `disable` | Disable hairpin NAT for this rule |

### Example

```yaml
one_to_one_nat_rules:
  # Web server - bidirectional 1:1 NAT
  - external: 203.0.113.10
    source_net: 192.168.1.100
    interface: wan
    nat_type: binat
    natreflection: enable
    description: Web server 1:1 NAT

  # Mail server
  - external: 203.0.113.11
    source_net: 192.168.1.101
    description: Mail server 1:1 NAT

  # Inbound only NAT
  - external: 203.0.113.12
    source_net: 192.168.1.102
    nat_type: nat
    description: Backup server inbound only
```

### Notes

- **Fully managed**: NAT rules can be created, updated, and deleted via API
- Changes are automatically applied after each operation
- Use `description` for reliable rule matching
- `external` must be an IP address available on the WAN interface
- For bidirectional NAT (`binat`), both inbound and outbound traffic is translated

---

## DNAT Rules (Port Forward)

DNAT (Destination NAT) rules forward incoming traffic from external ports to internal hosts. Also known as port forwarding. **Fully managed** via API.

### Schema

```yaml
dnat_rules:
  - uuid: <string>           # Optional: UUID for exact matching
    target: <string>         # Required: internal IP to forward to
    local_port: <integer>    # Optional: internal port to forward to
    interface: <list>        # Optional: interfaces (default: [wan])
    disabled: <boolean>      # Optional: default false
    nordr: <boolean>         # Optional: no redirect (default: false)
    protocol: <string>       # Optional: tcp, udp, tcp/udp
    ipprotocol: <string>     # Optional: inet, inet6, inet46 (default: inet)
    natreflection: <string>  # Optional: purenat, disable
    poolopts: <string>       # Optional: pool options for multiple targets
    sequence: <integer>      # Optional: rule order (1-999999)
    log: <boolean>           # Optional: log matches (default: false)
    descr: <string>          # Recommended: for rule matching
```

### IP Protocol

| Value | Description |
|-------|-------------|
| `inet` | IPv4 only (default) |
| `inet6` | IPv6 only |
| `inet46` | Both IPv4 and IPv6 |

### NAT Reflection

| Value | Description |
|-------|-------------|
| `purenat` | Use pure NAT for reflection |
| `disable` | Disable NAT reflection for this rule |

### Pool Options

For rules with multiple targets (load balancing):

| Value | Description |
|-------|-------------|
| `round-robin` | Round-robin distribution |
| `round-robin sticky-address` | Round-robin with sticky sessions |
| `random` | Random distribution |
| `random sticky-address` | Random with sticky sessions |
| `source-hash` | Hash based on source address |
| `bitmask` | Bitmask-based selection |

### Example

```yaml
dnat_rules:
  # Web server port forward (HTTP)
  - target: 192.168.1.100
    local_port: 80
    interface:
      - wan
    protocol: tcp
    descr: Web server HTTP

  # Web server port forward (HTTPS)
  - target: 192.168.1.100
    local_port: 443
    interface:
      - wan
    protocol: tcp
    descr: Web server HTTPS

  # SSH port forward
  - target: 192.168.1.50
    local_port: 22
    interface:
      - wan
    protocol: tcp
    log: true
    descr: SSH access to server

  # Game server (UDP)
  - target: 192.168.1.200
    local_port: 27015
    interface:
      - wan
    protocol: udp
    descr: Game server
```

### Notes

- **Fully managed**: DNAT rules can be created, updated, and deleted via API
- Changes are automatically applied after each operation
- Use `descr` for reliable rule matching (note: `descr` not `description`)
- `interface` is a list - use `[wan]` for single interface
- For bi-directional access (hairpin NAT), configure `natreflection`
- The `nordr` option disables actual redirection (useful for logging only)

---

## Complete Example

```yaml
# =============================================================================
# OPNsense Configuration - Production Environment
# =============================================================================

dns_hosts:
  - hostname: nas
    domain: lan
    ip: 192.168.1.10
    description: Synology NAS

  - hostname: proxmox
    domain: lan
    ip: 192.168.1.20
    description: Proxmox VE Host

  - hostname: pihole
    domain: lan
    ip: 192.168.1.5
    description: Pi-hole DNS

dhcp_reservations:
  - mac: aa:bb:cc:dd:ee:01
    ip: 192.168.1.10
    hostname: nas

  - mac: aa:bb:cc:dd:ee:02
    ip: 192.168.1.20
    hostname: proxmox

  - mac: aa:bb:cc:dd:ee:03
    ip: 192.168.1.5
    hostname: pihole

firewall_aliases:
  - name: internal_networks
    type: network
    content:
      - 192.168.1.0/24
      - 192.168.2.0/24
    description: All internal networks

  - name: dns_servers
    type: host
    content:
      - 192.168.1.5
      - 1.1.1.1
      - 8.8.8.8
    description: Allowed DNS servers

  - name: management_ports
    type: port
    content:
      - "22"
      - "443"
      - "8006"
    description: Management ports (SSH, HTTPS, Proxmox)

firewall_rules:
  - action: pass
    interface:
      - lan
    source: internal_networks
    destination: dns_servers
    protocol: udp
    destination_port: "53"
    description: Allow DNS to approved servers

  - action: pass
    interface:
      - lan
    source: 192.168.1.0/24
    destination: 192.168.1.20
    protocol: tcp
    destination_port: "8006"
    description: Allow Proxmox access from LAN

  - action: block
    interface:
      - lan
    destination: any
    protocol: udp
    destination_port: "53"
    description: Block DNS to other servers
    log: true
```

---

## Exporting Current State

You can export the current OPNsense configuration to YAML:

```python
state = client.state()

# Export to string
yaml_content = state.export_yaml()
print(yaml_content)

# Export to file
state.export_yaml_to_file('backup_config.yaml')

# Export specific entity types only
state.export_yaml_to_file('dns_only.yaml', entity_types=['dns_host'])
```

---

## API Reference

### Loading State

```python
# From file
state.load_yaml('config.yaml')

# From string
state.load_yaml_string(yaml_content)

# Method chaining
state.load_yaml('config.yaml').plan()
```

### Planning and Applying

```python
# Compare desired vs actual
changes = state.plan()

# Print human-readable plan
print(state.format_plan(changes))

# Apply all changes
state.apply(auto_approve=True)

# Apply with confirmation callback
def confirm(change, auto):
    print(f"Apply {change.change_type}: {change.name}?")
    return input("y/n: ").lower() == 'y'

state.apply(on_change=confirm)
```

### Exporting State

```python
# To YAML string
yaml_str = state.export_yaml()

# To YAML file
state.export_yaml_to_file('output.yaml')

# To Python code
python_code = state.export()
state.export_to_file('output.py')
```
