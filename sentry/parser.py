import json
import os
from pathlib import Path

SENTRY_DIR = Path(os.environ["APPDATA"]) / ".sentry"
DEFAULT_SALT = SENTRY_DIR / "salt"
CONFIG_FILE = SENTRY_DIR / "settings.json"


def read_config(key):
    with open(CONFIG_FILE, "r") as config:
        settings = json.loads(config.read())
        if key in settings:
            return settings[key]
        return "invalid setting key"


def write_config(key, value):
    with open(CONFIG_FILE, "r") as config:
        settings = json.loads(config.read())

    if key in settings:
        settings[key] = value
    else:
        return False

    with open(CONFIG_FILE, "w") as config:
        config.write(json.dumps(settings))
    return True


DEFAULT_VAULT = read_config("db_path")
