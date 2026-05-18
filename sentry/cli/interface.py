import getpass

from sentry.vault.vault_manager import (
    add_new_vault_data,
    fetch_vault_data,
    get_credential_list,
    remove_vault_data,
    update_vault_data,
)


def fetch_credentials(key):
    valid = False
    print()
    while not valid:
        id = input("Enter credential ID (leave blank to esc): ").lower()
        if id == "":
            print()
            return
        credentials = fetch_vault_data(key, id)
        if credentials is None:
            print("Invalid credential identifier.")
        else:
            print(f"Identifier:\t{credentials.get('id').lower().title()}")
            print(f"Username:\t{credentials.get('username')}")
            print(f"Password:\t{credentials.get('password')}")
            break
    print()


def add_new_credentials(key):
    result = None
    print()
    while result is None:
        id = input("Enter identifier (leave blank to esc): ")
        if id == "":
            print()
            return
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ", echo_char="*")
        result = add_new_vault_data(key, id, username, password)
    print("Credentials added successfully.")
    print()


def update_credentials(key):
    result = None
    print()
    while result is None:
        id = input("Enter credential identifier (leave blank to esc): ")
        if id == "":
            print()
            return
        username = input("Enter updated username: ")
        password = getpass.getpass("Enter updated password: ", echo_char="*")
        result = update_vault_data(key, id, username, password)
    print("Credentials updated successfully.")
    print()


def remove_credentials(key):
    result = None
    print()
    while result is None:
        id = input("Enter credential identifier (leave blank to esc): ")
        if id == "":
            print()
            return
        result = remove_vault_data(key, id)
    print("Credentials removed successfully.")
    print()


def fetch_credential_list(key):
    print()
    result = get_credential_list(key)
    for i in range(len(result)):
        print(f"- {result[i].lower().title()}")
    print()
