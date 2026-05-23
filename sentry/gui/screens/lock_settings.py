import customtkinter

from sentry.gui.dialogs.reset_dialog import reset_sentry_application
from sentry.parser import write_config


class LockSettings(customtkinter.CTkFrame):
    def __init__(self, master, parent):
        super().__init__(master=master)
        self.grid_rowconfigure((1, 2, 3), weight=2, uniform="a")
        self.grid_rowconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure((1, 2), weight=5, uniform="a")
        self.grid_columnconfigure((0, 3), weight=1, uniform="a")

        self.header = self.generate_header()
        self.settings = self.generate_settings(parent)
        self.options = self.generate_options(parent)

        self.header.grid(row=0, column=1, columnspan=2, sticky="we")
        self.settings.grid(row=1, column=1, sticky="new", columnspan=2, rowspan=2)
        self.options.grid(row=2, column=2, sticky="se")

    def generate_header(self):
        header_frame = customtkinter.CTkFrame(self)
        settings_label = customtkinter.CTkLabel(
            header_frame, text="Settings", font=("Lexend Bold", 28)
        )
        hr = customtkinter.CTkFrame(header_frame, height=4)

        settings_label.pack(anchor="w", pady=(0, 16))
        hr.pack(anchor="s", fill="both")
        return header_frame

    def generate_settings(self, master):
        settings_frame = customtkinter.CTkFrame(self)

        appearance = customtkinter.CTkFrame(settings_frame)
        appearance_text = customtkinter.CTkLabel(
            appearance, text="Appearance", font=("Lexend Bold", 24)
        )
        l_frame = customtkinter.CTkFrame(
            appearance, corner_radius=10, fg_color=("#f0f0f0", "#282828")
        )
        d_frame = customtkinter.CTkFrame(
            appearance, corner_radius=10, fg_color=("#f0f0f0", "#282828")
        )
        light_mode = customtkinter.CTkRadioButton(
            l_frame,
            text="Light Mode",
            radiobutton_height=16,
            radiobutton_width=16,
            hover=False,
            variable=master.theme,
            value="light",
        )
        dark_mode = customtkinter.CTkRadioButton(
            d_frame,
            text="Dark Mode",
            radiobutton_height=16,
            radiobutton_width=16,
            hover=False,
            variable=master.theme,
            value="dark",
        )

        appearance_text.pack(pady=10, anchor="w")
        light_mode.pack(fill="both", padx=20, pady=20)
        dark_mode.pack(fill="both", padx=20, pady=20)
        l_frame.pack(fill="both", pady=(10, 0))
        d_frame.pack(fill="both", pady=(10, 0))
        appearance.pack(expand=True, fill="both", anchor="w")

        reset = customtkinter.CTkFrame(settings_frame)
        reset_text = customtkinter.CTkLabel(
            reset, text="Reset", font=("Lexend Bold", 24)
        )
        reset_frame = customtkinter.CTkFrame(reset, corner_radius=10)
        reset_frame.grid_columnconfigure(0, weight=3)
        reset_frame.grid_columnconfigure(1, weight=1)
        reset_desc = customtkinter.CTkLabel(
            reset_frame,
            text="If you have forgotten your master password.",
        )
        reset_btn = customtkinter.CTkButton(
            reset_frame,
            text="Reset",
            fg_color="#b00000",
            text_color="white",
            hover=False,
            height=32,
            corner_radius=4,
            command=lambda: reset_sentry_application(reset_desc),
        )
        reset_text.pack(pady=(26, 0), anchor="w")
        reset_desc.grid(row=0, column=0, sticky="w")
        reset_btn.grid(row=0, column=1, sticky="e")
        reset_frame.pack(fill="both", pady=(10, 0))
        reset.pack(expand=True, fill="both")

        return settings_frame

    def generate_options(self, master):
        def save_settings():
            write_config("appearance", master.theme.get())
            customtkinter.set_appearance_mode(master.theme.get().title())
            self.destroy()

        options_frame = customtkinter.CTkFrame(self)
        options_frame.grid_columnconfigure((0), weight=8)
        options_frame.grid_columnconfigure((1, 2), weight=1)
        save_btn = customtkinter.CTkButton(
            options_frame,
            text="Save changes",
            height=32,
            hover=False,
            corner_radius=4,
            command=save_settings,
        )
        cancel_btn = customtkinter.CTkButton(
            options_frame,
            text="Cancel",
            hover=False,
            height=32,
            corner_radius=4,
            command=self.destroy,
            fg_color=("#f0f0f0", "#282828"),
            text_color=("#282828", "#ffffff"),
        )

        save_btn.grid(row=0, column=2)
        cancel_btn.grid(row=0, column=1, padx=16)
        return options_frame
