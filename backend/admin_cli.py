"""Admin CLI — register users, list users, manage access.

Usage:
    python -m backend.admin_cli register "John Doe"
    python -m backend.admin_cli register "Jane" --email jane@example.com
    python -m backend.admin_cli list
    python -m backend.admin_cli deactivate LAI-A1B2C3D4
"""

from __future__ import annotations

import argparse
import sys

from backend.config import get_config
from backend.db import create_db


def main():
    parser = argparse.ArgumentParser(description="LoopedAI Admin CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # Register
    reg = sub.add_parser("register", help="Register a new user")
    reg.add_argument("name", help="User's display name")
    reg.add_argument("--email", help="Optional email address")

    # List
    sub.add_parser("list", help="List all registered users")

    # Deactivate
    deact = sub.add_parser("deactivate", help="Deactivate a user")
    deact.add_argument("looped_id", help="LoopedAI ID to deactivate")

    args = parser.parse_args()
    cfg = get_config()
    db = create_db(cfg.supabase_url, cfg.supabase_key)
    db.init_schema()

    if args.command == "register":
        lid = db.register_user(args.name, args.email)
        print(f"\n✅ Registered: {args.name}")
        print(f"   LoopedAI ID: {lid}")
        print(f"   Share this ID to access @loopedaibot\n")

    elif args.command == "list":
        users = db.list_users()
        if not users:
            print("No users registered.")
            return
        print(f"\n{'ID':<15} {'Name':<20} {'Telegram':<15} {'Plan':<8} {'Active'}")
        print("─" * 70)
        for u in users:
            active = "✅" if u.get("active", True) else "❌"
            print(
                f"{u['looped_id']:<15} {u['name']:<20} "
                f"{(u.get('telegram_id') or '-'):<15} "
                f"{u.get('plan', 'free'):<8} {active}"
            )
        print()

    elif args.command == "deactivate":
        if db.deactivate_user(args.looped_id):
            print(f"✅ Deactivated: {args.looped_id.upper()}")
        else:
            print(f"❌ User not found: {args.looped_id}")
            sys.exit(1)


if __name__ == "__main__":
    main()
