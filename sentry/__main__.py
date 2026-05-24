import sys
from textwrap import dedent
import tkinter
from tkinter import simpledialog

from sentry.vault.vault_manager import check_default_vault, generate_default_vault


def check_first_run():
    if not check_default_vault():
        root = tkinter.Tk()
        root.withdraw()
        master_password = simpledialog.askstring(
            title="Sentry Setup",
            prompt=dedent("""
                    Welcome to Sentry, a local password manager. You are
                    requested to set the MASTER PASSWORD, which you will
                    further use to lock and unlock the vault. Remember,
                    if you forget it, there is no recovery.\n"""),
            show="●",
            parent=root,
        )
        if master_password is None or not master_password:
            sys.exit(0)
        username = simpledialog.askstring(
            title="Sentry Setup",
            prompt="\n  Enter your username (limit: 15 characters)  \n",
        )
        if username is None or not username:
            sys.exit(0)
        if len(username) > 15:
            username = username[0:15]
        generate_default_vault(master_password, username)
        root.destroy()


if __name__ == "__main__":
    check_first_run()
    from sentry.gui.app import App

    app = App()
    app.mainloop()
