# Sentry CLI

A lightweight local password manager built with Python.

Sentry securely stores credentials in an encrypted vault on the user's device using a master password.
All encryption and decryption happen locally.

---

# Features

- Local encrypted password vault
- Master-password based encryption
- Secure key derivation using Argon2id
- AES-based authenticated encryption via Fernet
- No password recovery mechanism

---

# Security Model

- Vault data is encrypted locally
- Master password is never stored
- Encryption keys are derived using Argon2id
- Decryption only occurs in memory
- If the master password is lost, the vault cannot be recovered

---

## Windows Installer

Download the latest installer from the GitHub Releases page.

---

# Running From Source

## Requirements

- Python 3.13+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m sentry
```

---

# First Launch

On first launch, Sentry will:

1. Create the application directory
2. Generate a cryptographic salt
3. Create an encrypted vault
4. Ask for a master password

---

# Usage

Launch:

```bash
python -m sentry
```

Available operations:

- Fetch credentials
- Add credentials
- Update credentials
- Remove credentials
- View credential list

---

# CLI Commands

## Help

```
python -m sentry help
```

Displays usage information.

---

## Reset

```
python -m sentry reset
```

Permanently deletes:
- encrypted vault data
- stored application data

This action cannot be undone.

---

# Technologies Used

- Python
- Argon2id
- cryptography (Fernet)
- Nuitka (compile)

---

# License

MIT License

---

# Author

GitHub: https://github.com/kdx-08
