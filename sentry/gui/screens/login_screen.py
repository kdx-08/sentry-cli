from pathlib import Path
import sys

import customtkinter
from PIL import Image

from sentry.gui.screens.lock_settings import LockSettings
from sentry.vault.vault_manager import unlock_default_vault

img_path = (
    Path(__file__).resolve().parent.parent.parent / "assets" / "img" / "sentry-ico.png"
)
ds_path = (
    Path(__file__).resolve().parent.parent.parent
    / "assets"
    / "img"
    / "settings-dark.png"
)
ls_path = (
    Path(__file__).resolve().parent.parent.parent
    / "assets"
    / "img"
    / "settings-light.png"
)


class Login(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2), weight=3, uniform="a")
        self.grid_rowconfigure((0, 2), weight=2, uniform="a")
        self.grid_rowconfigure(1, weight=3, uniform="a")

        self.incorrect_count = 0
        self.settings = self.generate_settings_widget(master)
        self.login_widget = self.generate_login_widget(master)

        self.settings.grid(row=0, column=2, sticky="ne")
        self.login_widget.grid(row=1, column=1, sticky="news")

    def generate_settings_widget(self, master):
        def settings_command():
            self.settings = LockSettings(self, master)
            self.settings.grid(row=0, column=0, sticky="news", columnspan=3, rowspan=3)

        settings_frame = customtkinter.CTkFrame(self)
        settings_icon_img = customtkinter.CTkImage(
            light_image=Image.open(ds_path),
            dark_image=Image.open(ls_path),
            size=(16, 16),
        )
        settings_option = customtkinter.CTkButton(
            settings_frame,
            text="",
            image=settings_icon_img,
            width=16,
            height=16,
            fg_color="transparent",
            hover=False,
            command=settings_command,
        )

        settings_option.pack(anchor="e", padx=12, pady=8)
        return settings_frame

    def generate_login_widget(self, master):
        def validate_command():
            try:
                validated = (
                    str(type(unlock_default_vault(password_entry.get())))
                    == "<class 'dict'>"
                )
                if validated:
                    master.master_password = password_entry.get()
                    master.dashboard_screen()
                else:
                    raise Exception()
            except Exception:
                self.incorrect_count += 1
                password_entry.delete(0, "end")
                error_msg.configure(text=f"Wrong attempt: {self.incorrect_count}")
                if self.incorrect_count == 10:
                    sys.exit(-1)  # should reset after 10 failed attempts

        sentry_logo_img = customtkinter.CTkImage(
            light_image=Image.open(img_path),
            dark_image=Image.open(img_path),
            size=(60, 60),
        )
        login_frame = customtkinter.CTkFrame(self)
        sentry_logo = customtkinter.CTkLabel(
            login_frame, text="", image=sentry_logo_img
        )

        sentry_text = customtkinter.CTkLabel(
            login_frame,
            text="Sentry",
            width=200,
            height=30,
            font=("Lexend Bold", 28),
        )
        password_entry = customtkinter.CTkEntry(
            login_frame,
            width=300,
            height=40,
            corner_radius=4,
            placeholder_text="Master Password",
            show="●",
        )
        validate_btn = customtkinter.CTkButton(
            login_frame,
            width=300,
            height=40,
            text="Unlock",
            corner_radius=4,
            command=validate_command,
        )
        error_msg = customtkinter.CTkLabel(login_frame, text="", text_color="red")

        sentry_logo.pack(pady=10)
        sentry_text.pack()
        password_entry.pack(pady=20)
        validate_btn.pack(pady=(0, 10))
        error_msg.pack(anchor="w", padx=10)
        return login_frame
