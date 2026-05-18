import ctypes
import json
import platform
import secrets
from pathlib import Path

from sentry.crypto.crypto_utils import decrypt, encrypt

SENTRY_DIR = Path.home() / ".sentry"
default_vault = SENTRY_DIR / "default.enc"
default_salt = SENTRY_DIR / "salt"


def reset_app_data():
    default_vault.unlink(missing_ok=True)
    default_salt.unlink(missing_ok=True)
    SENTRY_DIR.rmdir()
    return True


def check_default_vault():
    return default_vault.is_file()


def generate_default_vault(key: str):
    default_vault.parent.mkdir(parents=True, exist_ok=True)
    default_salt.parent.mkdir(parents=True, exist_ok=True)
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetFileAttributesW(str(SENTRY_DIR), 0x02)
    gen_salt = secrets.token_bytes(16)
    with open(default_salt, "wb") as file:
        file.write(gen_salt)
    data = json.dumps({"entries": []})
    encrypted_data = encrypt(data, key, gen_salt)
    with open(default_vault, "wb") as vault:
        vault.write(encrypted_data)


def unlock_default_vault(key):
    result = None
    with open(default_salt, "rb") as salt_file:
        salt = salt_file.read()
    with open(default_vault, "rb") as vault:
        payload = vault.read()
        decrypted_data = decrypt(payload, key, salt)
        result = json.loads(decrypted_data)
    return result


def write_vault_data(key, payload):
    with open(default_salt, "rb") as salt_file:
        salt = salt_file.read()
    with open(default_vault, "wb") as vault:
        json_payload = json.dumps(payload)
        encrypted_data = encrypt(json_payload, key, salt)
        vault.write(encrypted_data)
    return True


def fetch_vault_data(key, id):
    payload = unlock_default_vault(key)
    for entry in payload["entries"]:
        if entry.get("id") == id.lower():
            return entry
    return None


def add_new_vault_data(key, id, username, password):
    id = id.lower()
    payload = unlock_default_vault(key)
    if id in get_credential_list(key):
        print("Identifier exists, try another one.")
        return None
    payload["entries"].append({"id": id, "username": username, "password": password})
    return write_vault_data(key, payload)


def update_vault_data(key, id, username, password):
    id = id.lower()
    payload = unlock_default_vault(key)
    if id not in get_credential_list(key):
        print("Identifer does not exist. Try again.")
        return None
    for entry in payload["entries"]:
        if entry.get("id") == id:
            entry["username"] = username
            entry["password"] = password
    return write_vault_data(key, payload)


def remove_vault_data(key, id):
    id = id.lower()
    payload = unlock_default_vault(key)
    if id not in get_credential_list(key):
        print("Identifier does not exist. Try again.")
        return None
    index = 0

    for entry in payload["entries"]:
        if entry.get("id") == id:
            payload["entries"].remove(entry)
            break
        index += 1
    return write_vault_data(key, payload)


def get_credential_list(key):
    payload = unlock_default_vault(key)
    cred_list = []
    for entry in payload["entries"]:
        cred_list.append(entry["id"].lower())
    return cred_list
