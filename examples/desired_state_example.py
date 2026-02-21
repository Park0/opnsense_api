#!/usr/bin/env python3
"""
Example: Desired State Configuration for OPNsense

This example demonstrates how to use the StateManager to declare
desired network state and apply changes to OPNsense.
"""
import os
import sys

# Add parent directory to path for local development
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opnsense_api.client import Client
from opnsense_api.state import StateManager, ChangeType


def main():
    # Initialize client (use environment variables for credentials)
    client = Client(
        api_key=os.environ.get('OPNSENSE_API_KEY', 'your-api-key'),
        api_secret=os.environ.get('OPNSENSE_API_SECRET', 'your-api-secret'),
        base_url=os.environ.get('OPNSENSE_URL', 'https://opnsense.local/api'),
        verify_cert=False
    )

    # Create state manager
    # You can also use: state = client.state()
    state = StateManager(client)

    # =================================================================
    # EXAMPLE 1: Declare DNS host overrides
    # =================================================================
    print("Declaring desired DNS hosts...")

    state.dns_host(
        hostname='server1',
        domain='lan',
        ip='192.168.1.100',
        description='Application server'
    )

    state.dns_host(
        hostname='server2',
        domain='lan',
        ip='192.168.1.101',
        description='Database server'
    )

    state.dns_host(
        hostname='nas',
        domain='lan',
        ip='192.168.1.10',
        description='Network storage'
    )

    # =================================================================
    # EXAMPLE 2: Declare DHCP reservations
    # =================================================================
    print("Declaring desired DHCP reservations...")

    state.dhcp_reservation(
        mac='aa:bb:cc:dd:ee:ff',
        ip='192.168.1.50',
        hostname='printer',
        description='Office printer'
    )

    state.dhcp_reservation(
        mac='11:22:33:44:55:66',
        ip='192.168.1.51',
        hostname='scanner',
        description='Document scanner'
    )

    # =================================================================
    # EXAMPLE 3: Declare firewall aliases
    # =================================================================
    print("Declaring desired firewall aliases...")

    state.firewall_alias(
        name='webservers',
        type='host',
        content=['10.0.0.1', '10.0.0.2', '10.0.0.3'],
        description='Production web servers'
    )

    state.firewall_alias(
        name='trusted_networks',
        type='network',
        content=['192.168.1.0/24', '10.0.0.0/8'],
        description='Trusted internal networks'
    )

    # =================================================================
    # PLAN: Compare desired vs actual state
    # =================================================================
    print("\n" + "=" * 60)
    print("PLANNING CHANGES")
    print("=" * 60)

    changes = state.plan()

    # Print formatted plan
    print(state.format_plan(changes))

    # =================================================================
    # ANALYZE: Process changes programmatically
    # =================================================================
    creates = [c for c in changes if c.change_type == ChangeType.CREATE]
    updates = [c for c in changes if c.change_type == ChangeType.UPDATE]
    matches = [c for c in changes if c.change_type == ChangeType.MATCH]
    ambiguous = [c for c in changes if c.change_type == ChangeType.AMBIGUOUS]

    if ambiguous:
        print("\n" + "=" * 60)
        print("AMBIGUOUS MATCHES (require manual resolution)")
        print("=" * 60)
        for change in ambiguous:
            print(f"\n{change.entity_type}: {change.name}")
            print(f"  Desired: {change.desired}")
            print(f"  Found {len(change.alternatives)} potential matches:")
            for i, alt in enumerate(change.alternatives):
                print(f"    [{i+1}] {alt}")
            print("  Options: Choose a match, create new, or skip")

    # =================================================================
    # APPLY: Execute changes (with confirmation)
    # =================================================================
    if creates or updates:
        print("\n" + "=" * 60)
        print("APPLYING CHANGES")
        print("=" * 60)

        def confirm_change(change, auto_approve):
            """Interactive confirmation callback"""
            if change.change_type == ChangeType.CREATE:
                action = "Create"
            elif change.change_type == ChangeType.UPDATE:
                action = "Update"
            else:
                return False

            # In this example, we'll auto-approve all changes
            # In production, you might want to prompt the user
            print(f"  {action} {change.entity_type}: {change.name}")
            return True

        # Apply with confirmation callback
        # Set auto_approve=True to apply without confirmation
        # applied = state.apply(auto_approve=True)

        # Apply with custom confirmation
        applied = state.apply(on_change=confirm_change)

        print(f"\nApplied {len(applied)} changes")
    else:
        print("\nNo changes to apply - system is in desired state!")


def example_chained_api():
    """Example of fluent/chained API style"""
    client = Client(
        api_key='key',
        api_secret='secret',
        base_url='https://opnsense.local/api'
    )

    # Chained declaration style
    changes = (
        client.state()
        .dns_host(hostname='server1', domain='lan', ip='192.168.1.100')
        .dns_host(hostname='server2', domain='lan', ip='192.168.1.101')
        .dhcp_reservation(mac='aa:bb:cc:dd:ee:ff', ip='192.168.1.50')
        .firewall_alias(name='servers', type='host', content=['192.168.1.100', '192.168.1.101'])
        .plan()
    )

    for change in changes:
        print(f"{change.change_type.value}: {change.entity_type} {change.name}")


def example_interactive_resolution():
    """Example of interactive ambiguous match resolution"""

    def resolve_ambiguous(change, auto_approve):
        """Interactive resolver for ambiguous matches"""
        if change.change_type != ChangeType.AMBIGUOUS:
            return auto_approve

        print(f"\nAmbiguous match for {change.entity_type} '{change.name}':")
        print(f"Desired: {change.desired}")
        print(f"\nPotential matches:")
        for i, alt in enumerate(change.alternatives):
            print(f"  [{i+1}] {alt}")
        print(f"  [0] Create new")
        print(f"  [s] Skip")

        choice = input("Select option: ").strip().lower()

        if choice == 's':
            return False
        elif choice == '0':
            # Force create new
            change.change_type = ChangeType.CREATE
            return True
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(change.alternatives):
                    # Update the matched entity instead
                    matched = change.alternatives[idx]
                    change.current = matched
                    change.change_type = ChangeType.UPDATE
                    # Get UUID from matched entity
                    change.uuid = str(getattr(matched, 'uuid', None))
                    return True
            except ValueError:
                pass

        return False


if __name__ == '__main__':
    main()
