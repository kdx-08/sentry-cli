from pathlib import Path

import customtkinter
from PIL import Image

from sentry.gui.dialogs.delete_dialog import delete_confirmation
from sentry.parser import tabularize_cred
from sentry.vault.vault_manager import unlock_default_vault

bin_path = Path(__file__).resolve().parent.parent.parent / "assets" / "img" / "bin.png"


class Passwords(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.cred_store = unlock_default_vault(master.master.master_password)
        self.label_frame = customtkinter.CTkFrame(self)
        self.label_frame.grid_columnconfigure((0, 1), weight=1)
        self.label = customtkinter.CTkLabel(
            self.label_frame, text="Passwords", font=("Lexend Bold", 28)
        )
        self.clear_clipboard = customtkinter.CTkButton(
            self.label_frame,
            text="Clear clipboard",
            fg_color="#b00000",
            hover_color="#a00000",
            command=lambda: self.clipboard_clear() or self.clipboard_append(""),
            corner_radius=8,
        )
        self.passwords_table = self.generate_passwords_table()
        self.label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsw")
        self.clear_clipboard.grid(
            row=0, column=1, padx=(0, 20), pady=(10, 0), sticky="nse"
        )
        self.label_frame.pack(fill="both")
        self.passwords_table.pack(padx=(20, 5), pady=15, fill="both", expand=True)

    def generate_passwords_table(self):
        bin_image = customtkinter.CTkImage(
            light_image=Image.open(bin_path), dark_image=Image.open(bin_path)
        )
        table_frame = customtkinter.CTkScrollableFrame(
            self,
            scrollbar_button_color=("#ffffff", "#1e1e1e"),
            scrollbar_button_hover_color=("#ffffff", "#1e1e1e"),
        )
        tabular_data = tabularize_cred(self.cred_store)
        table = customtkinter.CTkFrame(
            table_frame, border_width=0, fg_color=("#e0e0e0", "#282828")
        )
        table.grid_rowconfigure(
            tuple(range(len(tabular_data) + 1)), weight=1, uniform="a"
        )
        table.grid_columnconfigure((0, 2, 3), weight=2, uniform="a")
        table.grid_columnconfigure(1, weight=3, uniform="a")

        title_sitename = customtkinter.CTkLabel(table, text="Service")
        title_username = customtkinter.CTkLabel(table, text="Username")
        title_password = customtkinter.CTkLabel(table, text="Password")
        title_actions = customtkinter.CTkLabel(table, text="Actions")
        title_sitename.grid(row=0, column=0, padx=(10, 5), ipady=10, pady=1)
        title_username.grid(row=0, column=1, padx=(5, 5), ipady=10, pady=1)
        title_password.grid(row=0, column=2, padx=(5, 5), ipady=10, pady=1)
        title_actions.grid(row=0, column=3, padx=(5, 10), ipady=10, pady=1)

        for i in range(len(tabular_data)):
            idt = tabular_data[i][3]
            pwd = tabular_data[i][2]
            ctl = tabular_data[i][0]
            sitename = customtkinter.CTkLabel(
                table, text=tabular_data[i][0], fg_color=("#e0e0e0", "#282828")
            )
            username = customtkinter.CTkLabel(
                table, text=tabular_data[i][1], fg_color=("#e0e0e0", "#282828")
            )
            password = customtkinter.CTkButton(
                table,
                text=10 * "●",
                text_color=("#282828", "#e0e0e0"),
                fg_color=("#e0e0e0", "#282828"),
                hover_color=("#ffffff", "#1e1e1e"),
                command=lambda p=pwd: (
                    self.clipboard_clear() or self.clipboard_append(p)
                ),
                border_width=0,
            )
            actions = customtkinter.CTkButton(
                table,
                text="",
                image=bin_image,
                fg_color=("#e0e0e0", "#282828"),
                border_width=0,
                hover_color=("#ffffff", "#1e1e1e"),
                command=lambda id=idt, c=ctl: (
                    delete_confirmation(self, self.master.master.master_password, id, c)
                    or self.master.switch_passwords()
                ),
            )
            sitename.grid(row=i + 1, column=0, padx=(10, 0), ipady=10, sticky="news")
            username.grid(row=i + 1, column=1, padx=0, ipady=10, sticky="news")
            password.grid(row=i + 1, column=2, padx=0, ipady=10, sticky="news")
            actions.grid(row=i + 1, column=3, padx=(0, 10), ipady=10, sticky="news")

        table.pack(expand=True, fill="both")
        return table_frame
