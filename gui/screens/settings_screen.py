import customtkinter

from gui.dialogs.reset_dialog import reset_sentry_application
from sentry.parser import write_config
from sentry.vault.vault_manager import SENTRY_DIR


class Settings(customtkinter.CTkFrame):
    def __init__(self, master, parent):
        super().__init__(master=master)
        self.grid_rowconfigure((1, 2, 3, 4), weight=2, uniform="a")
        self.grid_rowconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure((1, 2), weight=18, uniform="a")
        self.grid_columnconfigure((0, 3), weight=1, uniform="a")

        self.header = self.generate_header()
        self.settings = self.generate_settings(parent)
        self.options = self.generate_options(parent)
        self.db_path = None

        self.header.grid(row=0, column=1, columnspan=2, sticky="we")
        self.settings.grid(row=1, column=1, sticky="news", columnspan=2, rowspan=3)
        self.options.grid(row=4, column=2, sticky="e")

    def generate_header(self):
        header_frame = customtkinter.CTkFrame(self)
        settings_label = customtkinter.CTkLabel(
            header_frame, text="Settings", font=("Lexend Bold", 28)
        )
        hr = customtkinter.CTkFrame(header_frame, height=4)

        settings_label.pack(anchor="w")
        hr.pack(anchor="s", fill="both")
        return header_frame

    def generate_settings(self, master):
        def browse_db_file():
            filedialog = customtkinter.filedialog.askopenfilename(
                initialdir=SENTRY_DIR, filetypes=[("ENC Files", "*.enc")]
            )
            db_desc_path.configure(text=filedialog)
            if filedialog != "":
                self.db_path = filedialog

        settings_frame = customtkinter.CTkScrollableFrame(
            self,
            scrollbar_button_color=("#ffffff", "#1e1e1e"),
            scrollbar_button_hover_color=("#ffffff", "#1e1e1e"),
        )

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

        appearance_text.pack(pady=(0, 10), anchor="w")
        light_mode.pack(fill="both", padx=20, pady=20)
        dark_mode.pack(fill="both", padx=20, pady=20)
        l_frame.pack(fill="both", pady=(10, 0))
        d_frame.pack(fill="both", pady=(10, 0))
        appearance.pack(expand=True, fill="both", anchor="w")

        db = customtkinter.CTkFrame(settings_frame)
        db_text = customtkinter.CTkLabel(db, text="Database", font=("Lexend Bold", 24))
        db_frame = customtkinter.CTkFrame(db)
        db_frame.grid_columnconfigure((0, 1, 2), weight=3, uniform="a")
        db_frame.grid_columnconfigure(3, weight=2, uniform="a")
        db_desc = customtkinter.CTkLabel(db, text="Database path")
        db_desc_path = customtkinter.CTkLabel(
            db_frame,
            text=master.db_path,
            anchor="w",
            fg_color=("#f0f0f0", "#282828"),
            height=40,
            corner_radius=8,
        )
        db_path_picker = customtkinter.CTkButton(
            db_frame, text="Browse", command=browse_db_file, corner_radius=8
        )

        db_text.pack(pady=10, anchor="w")
        db_desc.pack(pady=5, anchor="w")
        db_desc_path.grid(row=0, column=0, columnspan=3, sticky="news", padx=(0, 20))
        db_path_picker.grid(row=0, column=3, sticky="news")
        db_frame.pack(pady=10, fill="both")
        db.pack(pady=10, expand=True, fill="both")

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
            command=lambda: reset_sentry_application(reset_desc=reset_desc),
        )

        reset_text.pack(pady=(26, 0), anchor="w")
        reset_desc.grid(row=0, column=0, sticky="wn")
        reset_btn.grid(row=0, column=1, sticky="en")
        reset_frame.pack(fill="both", pady=(10, 0))
        reset.pack(expand=True, fill="both")

        return settings_frame

    def generate_options(self, master):
        def save_settings():
            write_config("appearance", master.theme.get())
            customtkinter.set_appearance_mode(master.theme.get().title())
            if self.db_path:
                write_config("db_path", self.db_path)
                master.db_path = self.db_path
            self.after(500, self.destroy())

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
