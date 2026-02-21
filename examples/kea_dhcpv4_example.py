#!/usr/bin/env python3
"""
Example: Kea DHCPv4 API usage

Demonstrates enabling Kea, creating subnets and reservations.
"""
from opnsense_api.client import Client
from opnsense_api.pydantic.KeaDhcpv4 import Subnet4, Reservation, General, Dhcpv4

# Initialize client
client = Client(
    base_url='https://your-opnsense.local/api',
    api_key='your-api-key',
    api_secret='your-api-secret',
    verify_cert=False
)

# Enable Kea DHCP on interface opt1
settings = Dhcpv4(
    general=General(
        enabled=True,
        interfaces=['opt1']
    )
)
client.kea_dhcpv4_set(settings)
print("Enabled Kea on opt1")

# Create a subnet
subnet = Subnet4(
    subnet="192.168.100.0/24",
    pools="192.168.100.100-192.168.100.200",
    description="Guest Network"
)
result = client.kea_dhcpv4_add_subnet(subnet)
subnet_uuid = result.uuid
print(f"Created subnet: {subnet_uuid}")

# Create a reservation (static lease)
reservation = Reservation(
    subnet=subnet_uuid,
    ip_address="192.168.100.10",
    hw_address="00:11:22:33:44:55",
    hostname="server1",
    description="Web Server"
)
result = client.kea_dhcpv4_add_reservation(reservation)
print(f"Created reservation: {result.uuid}")

# List all subnets
subnets = client.kea_dhcpv4_search_subnet()
for s in subnets.rows:
    print(f"Subnet: {s.subnet} - {s.description}")

# List all reservations
reservations = client.kea_dhcpv4_search_reservation()
for r in reservations.rows:
    print(f"Reservation: {r.hw_address} -> {r.ip_address} ({r.hostname})")

# Disable Kea DHCP
# settings = Dhcpv4(
#     general=General(
#         enabled=False,
#         interfaces=[]
#     )
# )
# client.kea_dhcpv4_set(settings)
