from tkinter import messagebox

from sentry.vault.vault_manager import remove_vault_data


def delete_confirmation(master, key, id, cred_title):
    dialog = messagebox.askokcancel(
        parent=master,
        title="Delete credential",
        message=f"Are you sure you want to delete {cred_title}?",
        icon="warning",
    )
    if dialog:
        remove_vault_data(key, id)
