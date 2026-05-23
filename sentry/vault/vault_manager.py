import ctypes
import json
import platform
import secrets

from cryptography.fernet import InvalidToken

from sentry.crypto.crypto_utils import decrypt, encrypt
from sentry.parser import CONFIG_FILE, DEFAULT_SALT, DEFAULT_VAULT, SENTRY_DIR


def reset_app_data():
    DEFAULT_VAULT.unlink(missing_ok=True)
    DEFAULT_SALT.unlink(missing_ok=True)
    CONFIG_FILE.unlink(missing_ok=True)
    SENTRY_DIR.rmdir()
    return True


def check_default_vault():
    return DEFAULT_VAULT.is_file()


def generate_default_vault(key: str, username):
    DEFAULT_VAULT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_SALT.parent.mkdir(parents=True, exist_ok=True)
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetFileAttributesW(str(SENTRY_DIR), 0x02)
    gen_salt = secrets.token_bytes(16)
    with open(DEFAULT_SALT, "wb") as file:
        file.write(gen_salt)
    data = json.dumps({"entries": {}})
    encrypted_data = encrypt(data, key, gen_salt)
    with open(DEFAULT_VAULT, "wb") as vault:
        vault.write(encrypted_data)
    with open(CONFIG_FILE, "w") as config:
        configuration = json.dumps(
            {"username": username, "appearance": "dark", "db_path": str(DEFAULT_VAULT)},
            indent=4,
        )
        config.write(configuration)


def unlock_default_vault(key):
    try:
        result = None
        with open(DEFAULT_SALT, "rb") as salt_file:
            salt = salt_file.read()
        with open(DEFAULT_VAULT, "rb") as vault:
            payload = vault.read()
            decrypted_data = decrypt(payload, key, salt)
            result = json.loads(decrypted_data)
    except InvalidToken:
        return False
    return result


def write_vault_data(key, payload):
    with open(DEFAULT_SALT, "rb") as salt_file:
        salt = salt_file.read()
    with open(DEFAULT_VAULT, "wb") as vault:
        json_payload = json.dumps(payload)
        encrypted_data = encrypt(json_payload, key, salt)
        vault.write(encrypted_data)
    return True


def fetch_vault_data(key, id):
    cred_store = unlock_default_vault(key)
    if id in cred_store["entries"]:
        return cred_store["entries"][id]
    return None


def add_new_vault_data(key, id, service, username, password, url):
    cred_store = unlock_default_vault(key)
    if id in get_credential_list(key):
        return None
    cred_store["entries"][id] = {
        "id": id,
        "service": service,
        "username": username,
        "password": password,
        "url": url,
    }
    return write_vault_data(key, cred_store)


def update_vault_data(key, id, service, username, password, url):
    cred_store = unlock_default_vault(key)
    if id not in get_credential_list(key):
        print("Identifer does not exist. Try again.")
        return None
    cred_store["entries"][id]["service"] = service
    cred_store["entries"][id]["username"] = username
    cred_store["entries"][id]["password"] = password
    cred_store["entries"][id]["url"] = url
    return write_vault_data(key, cred_store)


def remove_vault_data(key, id):
    cred_store = unlock_default_vault(key)
    if id not in get_credential_list(key):
        print("Identifier does not exist. Try again.")
        return None
    cred_store["entries"].pop(id)
    return write_vault_data(key, cred_store)


def get_credential_list(key):
    cred_store = unlock_default_vault(key)
    return list(cred_store["entries"].keys())
