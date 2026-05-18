import base64

from argon2 import low_level
from cryptography.fernet import Fernet


def generate_hash_key(key, salt):
    return low_level.hash_secret_raw(
        secret=key.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=low_level.Type.ID,
    )


def encrypt(data, key, salt):
    hash_key = generate_hash_key(key, salt)
    fernet_key = base64.urlsafe_b64encode(hash_key)
    f = Fernet(fernet_key)
    return f.encrypt(data.encode())


def decrypt(encrypted_data, key, salt):
    hash_key = generate_hash_key(key, salt)
    fernet_key = base64.urlsafe_b64encode(hash_key)
    f = Fernet(fernet_key)
    return f.decrypt(encrypted_data).decode()
