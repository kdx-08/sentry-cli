# Sentry

A local-first password manager built with Python.

Sentry securely stores credentials and notes using encrypted vaults protected by a master password.
No cloud sync, no telemetry, no external servers.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- Encrypted local vault
- Secure credential storage
- Password generator
- Modern desktop GUI
- Dark mode support
- Portable executable build
- Native Windows installer

---

## Tech Stack

- Python
- CustomTkinter
- Cryptography
- Argon2
- Nuitka
- Inno Setup

---

## Development

```bash
git clone https://github.com/kdx-08/sentry-cli.git

cd sentry-cli

python -m venv .venv

source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt

python -m sentry
```

---

## Security

- Vault data is encrypted locally
- No recovery mechanism
- No internet connectivity required
- No analytics or tracking

---

## License

MIT
