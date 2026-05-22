import json
from sentry.vault.vault_manager import CONFIG_FILE


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
