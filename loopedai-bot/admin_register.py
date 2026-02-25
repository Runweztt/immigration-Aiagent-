"""Admin tool to register users and manage LoopedAI IDs.

Usage:
    python admin_register.py register "John Doe"
    python admin_register.py register "Jane Doe" --email jane@example.com
    python admin_register.py list
    python admin_register.py deactivate LAI-A1B2C3D4
"""

import argparse
import sys

from loopedai_auth import deactivate_user, init_db, list_users, register_user


def cmd_register(args):
    """Register a new user."""
    looped_id = register_user(args.name, email=args.email)
    print(f"\n✅ User registered successfully!")
    print(f"   Name:        {args.name}")
    if args.email:
        print(f"   Email:       {args.email}")
    print(f"   LoopedAI ID: {looped_id}")
    print(f"\n📱 Share this ID with the user to access @loopedaibot on Telegram.")


def cmd_list(args):
    """List all registered users."""
    users = list_users()
    if not users:
        print("No users registered yet.")
        return

    print(f"\n{'ID':<16} {'Name':<20} {'Email':<25} {'Telegram':<15} {'Active'}")
    print("─" * 90)
    for u in users:
        active = "✅" if u["active"] else "❌"
        print(
            f"{u['looped_id']:<16} {u['name']:<20} {(u['email'] or '-'):<25} "
            f"{(u['telegram_id'] or '-'):<15} {active}"
        )
    print(f"\nTotal: {len(users)} users")


def cmd_deactivate(args):
    """Deactivate a user."""
    if deactivate_user(args.looped_id):
        print(f"✅ Deactivated user {args.looped_id}")
    else:
        print(f"❌ User {args.looped_id} not found")


def main():
    init_db()

    parser = argparse.ArgumentParser(description="LoopedAI Admin Tool")
    sub = parser.add_subparsers(dest="command", required=True)

    # register
    reg = sub.add_parser("register", help="Register a new user")
    reg.add_argument("name", help="User's name")
    reg.add_argument("--email", help="User's email", default=None)
    reg.set_defaults(func=cmd_register)

    # list
    lst = sub.add_parser("list", help="List all users")
    lst.set_defaults(func=cmd_list)

    # deactivate
    deact = sub.add_parser("deactivate", help="Deactivate a user")
    deact.add_argument("looped_id", help="LoopedAI ID to deactivate")
    deact.set_defaults(func=cmd_deactivate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
