#!/usr/bin/env python3
"""
Firewall Filter Rule CRUD Operations Example

Demonstrates how to create, read, update, and delete firewall filter rules
using the PySense OPNsense API client.

Usage:
    export OPNSENSE_API_KEY="your-api-key"
    export OPNSENSE_API_SECRET="your-api-secret"
    export OPNSENSE_URL="https://your-opnsense:443/api"
    python3 examples/firewall_filter_crud.py
"""
import os
import sys

from opnsense_api.client import Client
from opnsense_api.pydantic.Rule import Rule


def main():
    # Load credentials from environment variables
    api_key = os.environ.get('OPNSENSE_API_KEY')
    api_secret = os.environ.get('OPNSENSE_API_SECRET')
    base_url = os.environ.get('OPNSENSE_URL')

    if not all([api_key, api_secret, base_url]):
        print("Error: Set OPNSENSE_API_KEY, OPNSENSE_API_SECRET, and OPNSENSE_URL")
        sys.exit(1)

    # Initialize client
    client = Client(
        api_key=api_key,
        api_secret=api_secret,
        base_url=base_url,
        verify_cert=False,
        timeout=30
    )

    # -------------------------------------------------------------------------
    # CREATE: Add a new firewall rule
    # -------------------------------------------------------------------------
    print("Creating firewall rule...")

    new_rule = Rule(
        enabled=True,
        action=Rule.RulesRuleActionEnum.PASS,
        direction=Rule.RulesRuleDirectionEnum.IN,
        ipprotocol=Rule.RulesRuleIpprotocolEnum.INET,
        protocol="TCP",
        source_net=["any"],
        destination_net=["any"],
        destination_port="8080",
        sequence=50,
        description="Example rule - allow TCP 8080 inbound"
    )

    result = client.firewall_filter_add_rule(new_rule)
    uuid = result.uuid
    print(f"Created rule: {uuid}")

    # -------------------------------------------------------------------------
    # READ: Retrieve the rule by UUID
    # -------------------------------------------------------------------------
    print("\nReading rule...")

    rule = client.firewall_filter_get_rule(uuid)
    print(f"  Enabled: {rule.enabled}")
    print(f"  Action: {rule.action.value}")
    print(f"  Direction: {rule.direction.value}")
    print(f"  Protocol: {rule.protocol}")
    print(f"  Destination Port: {rule.destination_port}")
    print(f"  Sequence: {rule.sequence}")
    print(f"  Description: {rule.description}")

    # -------------------------------------------------------------------------
    # UPDATE: Modify the rule
    # -------------------------------------------------------------------------
    print("\nUpdating rule...")

    updated_rule = Rule(
        enabled=True,
        action=Rule.RulesRuleActionEnum.PASS,
        direction=Rule.RulesRuleDirectionEnum.IN,
        ipprotocol=Rule.RulesRuleIpprotocolEnum.INET,
        protocol="TCP",
        source_net=["any"],
        destination_net=["any"],
        destination_port="9090",
        sequence=50,
        description="Example rule - MODIFIED to TCP 9090"
    )

    result = client.firewall_filter_set_rule(uuid, updated_rule)
    print(f"Update result: {result.result}")

    # Verify the update
    rule = client.firewall_filter_get_rule(uuid)
    print(f"  New port: {rule.destination_port}")
    print(f"  New description: {rule.description}")

    # -------------------------------------------------------------------------
    # LIST: Search all filter rules
    # -------------------------------------------------------------------------
    print("\nListing all rules...")

    search_result = client.firewall_filter_search_rule()
    print(f"Total rules: {search_result.total}")
    for r in search_result.rows:
        status = "enabled" if r.enabled else "disabled"
        print(f"  [{r.uuid}] ({status}) {r.description or '(no description)'}")

    # -------------------------------------------------------------------------
    # DELETE: Remove the rule
    # -------------------------------------------------------------------------
    print("\nDeleting rule...")

    result = client.firewall_filter_del_rule(uuid)
    print(f"Delete result: {result.result}")

    # Verify deletion
    search_result = client.firewall_filter_search_rule()
    print(f"Rules remaining: {search_result.total}")

    # -------------------------------------------------------------------------
    # APPLY: Apply changes to activate rules (optional)
    # -------------------------------------------------------------------------
    # Uncomment to apply changes to the firewall:
    #
    # # Create savepoint for rollback capability
    # savepoint = client.firewall_filter_savepoint()
    # revision = savepoint.get('revision')
    #
    # # Apply changes
    # result = client.firewall_filter_apply(revision)
    # print(f"Apply result: {result.result}")
    #
    # # Or cancel rollback if something went wrong
    # # client.firewall_filter_cancel_rollback(revision)

    print("\nDone.")


if __name__ == "__main__":
    main()
