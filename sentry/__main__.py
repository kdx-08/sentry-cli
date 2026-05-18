import getpass
import sys
import time

from sentry.cli.interface import (
    add_new_credentials,
    fetch_credential_list,
    fetch_credentials,
    remove_credentials,
    update_credentials,
)
from sentry.vault.vault_manager import (
    check_default_vault,
    generate_default_vault,
    reset_app_data,
    unlock_default_vault,
)

MASTER_PASS = ""


def check_first_run():
    global MASTER_PASS
    if not check_default_vault():
        display_help()
        time.sleep(3)
        print("Initializing default vault...")
        time.sleep(1)
        MASTER_PASS = input("Set the master password: ")
        generate_default_vault(MASTER_PASS)
    unlock_vault()


def unlock_vault():
    global MASTER_PASS
    unlocked = False
    while not unlocked:
        MASTER_PASS = getpass.getpass("Enter master password: ", echo_char="*")
        try:
            unlock_default_vault(MASTER_PASS)
            unlocked = True
            start()
        except Exception:
            print("Failed to unlock vault.")
            print("Master password may be incorrect or vault file may be corrupted.\n")


def start():
    while True:
        print("1. Fetch credentials")
        print("2. Add new credentials")
        print("3. Update credentials")
        print("4. Remove credentials")
        print("5. View credential list")
        print("Enter anything else to quit.")
        choice = input("Enter your choice: ")
        if choice == "1":
            fetch_credentials(MASTER_PASS)
        elif choice == "2":
            add_new_credentials(MASTER_PASS)
        elif choice == "3":
            update_credentials(MASTER_PASS)
        elif choice == "4":
            remove_credentials(MASTER_PASS)
        elif choice == "5":
            fetch_credential_list(MASTER_PASS)
        else:
            raise KeyboardInterrupt


def display_help():
    print("""
Sentry is a local encrypted password vault manager.

All passwords are stored only on your device in an encrypted vault file.
Your master password is never stored anywhere.

IMPORTANT:

If you forget your master password, your vault cannot be recovered.
Keep your master password safe.
Do not manually edit or tamper the vault file.
Doing so could lead to permanent data loss.

BASIC WORKFLOW

On first launch, you will be asked to create a master password.
Enter your master password to decrypt and access stored entries.

You can:
- add passwords
- view stored entries
- update entries
- delete entries

COMMANDS

- help
    Display this help message.

- reset
    Permanently delete all stored vault data.
    The reset command permanently deletes:
        - encrypted vault data
        - saved application data
    This action cannot be undone.
""")


def reset_app():
    print("""
WARNING
This will permanently delete your encrypted vault and all stored passwords.
This action cannot be undone. You can press Ctrl+C to cancel this operation.
""")
    choice = input("Do you wish to continue (YES/NO): ")
    if choice != "YES":
        print("Cancelling operation...\n")
        return
    confirm = input("Enter DELETE to permanently remove vault data: ")
    if confirm != "DELETE":
        print("Cancelling operation...\n")
        return
    result = reset_app_data()
    if result:
        print("Sentry has been reset.\n")
        time.sleep(1)
        raise KeyboardInterrupt


if __name__ == "__main__":
    try:
        args = sys.argv
        if "help" in args or "--help" in args:
            display_help()
        elif "reset" in args or "--reset" in args:
            reset_app()
        elif len(sys.argv) > 1:
            print('Invalid argument. Available ["--help", "help", "--reset", "reset"]')
            sys.exit(-1)
        else:
            check_first_run()
    except KeyboardInterrupt:
        print("\nPowering off Sentry...")
        time.sleep(1)
        print("Bye.")
    sys.exit(0)
