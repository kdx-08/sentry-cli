import customtkinter

from sentry.generator import generate_id
from sentry.vault.vault_manager import add_new_vault_data, unlock_default_vault


class NewEntry(customtkinter.CTkFrame):
    def __init__(self, master, parent):
        super().__init__(master)
        self.form_title = customtkinter.CTkLabel(
            self, text="New Credential", font=("Lexend Bold", 28)
        )
        self.form = self.generate_form_widget(parent)
        self.form_title.pack(padx=20, pady=10, anchor="w")
        self.form.pack(padx=20, pady=(0, 155), fill="both", expand=True)

    def generate_form_widget(self, parent):
        def save_credential():
            cred_store = unlock_default_vault(parent.master_password)
            id = generate_id()
            while id in cred_store["entries"]:
                id = generate_id()
            if add_new_vault_data(
                parent.master_password,
                id,
                service_name.get(),
                username.get(),
                password.get(),
                url.get(),
            ):
                response.configure(
                    text="Credentials added successfully", text_color="#00aa00"
                )
            else:
                response.configure(text="Something went wrong", text_color="#aa0000")

            self.after(1000, self.destroy)

        form = customtkinter.CTkFrame(
            self, fg_color=("#e0e0e0", "#282828"), border_width=0, corner_radius=8
        )
        service_label = customtkinter.CTkLabel(form, text="Service name", anchor="w")
        service_name = customtkinter.CTkEntry(
            form, placeholder_text="e.g., Microsoft", height=40
        )
        username_label = customtkinter.CTkLabel(form, text="Username", anchor="w")
        username = customtkinter.CTkEntry(
            form, placeholder_text="e.g., user@outlook.com", height=40
        )
        password_label = customtkinter.CTkLabel(form, text="Password", anchor="w")
        password = customtkinter.CTkEntry(
            form, placeholder_text="Enter password", height=40
        )
        url_label = customtkinter.CTkLabel(form, text="URL", anchor="w")
        url = customtkinter.CTkEntry(
            form, placeholder_text="e.g., https://login.live.com", height=40
        )
        options_frame = customtkinter.CTkFrame(
            form, fg_color="transparent", border_width=0
        )
        options_frame.grid_columnconfigure((0), weight=2, uniform="a")
        options_frame.grid_columnconfigure((1, 2), weight=1, uniform="a")
        response = customtkinter.CTkLabel(options_frame, text="", anchor="w")
        save_btn = customtkinter.CTkButton(
            options_frame,
            text="Save",
            height=32,
            hover=False,
            corner_radius=4,
            command=save_credential,
        )
        cancel_btn = customtkinter.CTkButton(
            options_frame,
            text="Cancel",
            hover=False,
            height=32,
            corner_radius=4,
            command=self.destroy,
            fg_color="#b00000",
            text_color="#ffffff",
        )

        service_label.pack(padx=20, pady=(10, 2), fill="both")
        service_name.pack(padx=20, pady=(2, 10), fill="both")
        username_label.pack(padx=20, pady=(10, 2), fill="both")
        username.pack(padx=20, pady=(2, 10), fill="both")
        password_label.pack(padx=20, pady=(10, 2), fill="both")
        password.pack(padx=20, pady=(2, 10), fill="both")
        url_label.pack(padx=20, pady=(10, 2), fill="both")
        url.pack(padx=20, pady=(2, 10), fill="both")
        response.grid(padx=20, row=0, column=0, sticky="news")
        cancel_btn.grid(row=0, column=1)
        save_btn.grid(row=0, column=2)
        options_frame.pack(pady=(10, 20), fill="both", anchor="e")

        return form
