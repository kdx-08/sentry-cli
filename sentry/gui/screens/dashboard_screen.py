from pathlib import Path

import customtkinter
from PIL import Image

from sentry.gui.screens.generator_screen import Generator
from sentry.gui.screens.new_entry_screen import NewEntry

# from sentry.gui.screens.notes_screen import Notes
from sentry.gui.screens.passwords_screen import Passwords
from sentry.gui.screens.settings_screen import Settings

avatar_path = (
    Path(__file__).resolve().parent.parent.parent / "assets" / "img" / "avatar.png"
)
plus_path = (
    Path(__file__).resolve().parent.parent.parent / "assets" / "img" / "plus.png"
)

# dfile_path = (
#   Path(__file__).resolve().parent.parent.parent / "assets" / "img" / "file-dark.png"
# )
# lfile_path = (
#   Path(__file__).resolve().parent.parent.parent / "assets" / "img" / "file-light.png"
# )
dgenerator_path = (
    Path(__file__).resolve().parent.parent.parent
    / "assets"
    / "img"
    / "generator-dark.png"
)
lgenerator_path = (
    Path(__file__).resolve().parent.parent.parent
    / "assets"
    / "img"
    / "generator-light.png"
)
dlock_path = (
    Path(__file__).resolve().parent.parent.parent / "assets" / "img" / "lock-dark.png"
)
llock_path = (
    Path(__file__).resolve().parent.parent.parent / "assets" / "img" / "lock-light.png"
)
dsettings_path = (
    Path(__file__).resolve().parent.parent.parent
    / "assets"
    / "img"
    / "settings-dark.png"
)
lsettings_path = (
    Path(__file__).resolve().parent.parent.parent
    / "assets"
    / "img"
    / "settings-light.png"
)


class Dashboard(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=4, uniform="a")
        self.grid_rowconfigure(0, weight=1, uniform="a")
        self.grid_rowconfigure(1, weight=12, uniform="a")

        self.master = master
        self.sidebar = self.generate_sidebar(master)
        self.addentry = self.generate_add_entry()
        self.default = Passwords(self)
        self.mainframe = None
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="news")
        self.addentry.grid(row=0, column=1, sticky="news")
        self.default.grid(row=1, column=1, sticky="news")

    def generate_sidebar(self, master):
        sidebar = customtkinter.CTkFrame(
            self, fg_color=("#f0f0f0", "#282828"), border_color=("#f0f0f0", "#282828")
        )
        avatar_frame = customtkinter.CTkFrame(
            sidebar, fg_color="transparent", border_color=("#f0f0f0", "#282828")
        )
        avatar_logo_img = customtkinter.CTkImage(
            light_image=Image.open(avatar_path),
            dark_image=Image.open(avatar_path),
            size=(40, 40),
        )
        avatar_logo = customtkinter.CTkLabel(
            avatar_frame, text="", image=avatar_logo_img
        )
        avatar_text = customtkinter.CTkLabel(avatar_frame, text=master.username)
        avatar_logo.grid(row=0, column=0, padx=(20, 10), sticky="w")
        avatar_text.grid(row=0, column=1)
        avatar_frame.pack(pady=10, fill="both")

        menu_frame = customtkinter.CTkFrame(
            sidebar, fg_color="transparent", border_color=("#f0f0f0", "#282828")
        )
        password_icon = customtkinter.CTkImage(
            light_image=Image.open(dlock_path), dark_image=Image.open(llock_path)
        )
        # notes_icon = customtkinter.CTkImage(
        #     light_image=Image.open(dfile_path), dark_image=Image.open(lfile_path)
        # )
        generator_icon = customtkinter.CTkImage(
            light_image=Image.open(dgenerator_path),
            dark_image=Image.open(lgenerator_path),
        )
        settings_icon = customtkinter.CTkImage(
            light_image=Image.open(dsettings_path),
            dark_image=Image.open(lsettings_path),
        )
        passwords = customtkinter.CTkButton(
            menu_frame,
            text="Passwords",
            image=password_icon,
            compound="left",
            fg_color="transparent",
            anchor="w",
            hover_color=("#e0e0e0", "#1e1e1e"),
            height=50,
            corner_radius=8,
            text_color=("#1e1e1e", "#ffffff"),
            command=self.switch_passwords,
        )
        # notes = customtkinter.CTkButton(
        #     menu_frame,
        #     text="Secure Notes",
        #     image=notes_icon,
        #     compound="left",
        #     fg_color="transparent",
        #     anchor="w",
        #     hover_color=("#e0e0e0", "#1e1e1e"),
        #     height=50,
        #     corner_radius=8,
        #     text_color=("#1e1e1e", "#ffffff"),
        #     command=self.switch_notes,
        # )
        generator = customtkinter.CTkButton(
            menu_frame,
            text="Generator",
            image=generator_icon,
            compound="left",
            fg_color="transparent",
            anchor="w",
            hover_color=("#e0e0e0", "#1e1e1e"),
            height=50,
            corner_radius=8,
            text_color=("#1e1e1e", "#ffffff"),
            command=self.switch_generator,
        )
        settings = customtkinter.CTkButton(
            menu_frame,
            text="Settings",
            image=settings_icon,
            compound="left",
            fg_color="transparent",
            anchor="w",
            hover_color=("#e0e0e0", "#1e1e1e"),
            height=50,
            corner_radius=8,
            text_color=("#1e1e1e", "#ffffff"),
            command=self.switch_settings,
        )

        passwords.pack(pady=(5, 0), expand=True, fill="both")
        # notes.pack(pady=5, expand=True, fill="both")
        generator.pack(pady=(0, 5), expand=True, fill="both")
        settings.pack(expand=True, fill="both")

        menu_frame.pack(padx=10, pady=20, fill="both")
        return sidebar

    def generate_add_entry(self):
        entry_frame = customtkinter.CTkFrame(
            self, fg_color=("#f0f0f0", "#282828"), border_color=("#f0f0f0", "#282828")
        )
        plus_icon = customtkinter.CTkImage(
            light_image=Image.open(plus_path),
            dark_image=Image.open(plus_path),
            size=(14, 14),
        )
        new_entry_btn = customtkinter.CTkButton(
            entry_frame,
            text="Add Entry",
            height=36,
            width=100,
            corner_radius=8,
            image=plus_icon,
            compound="left",
            command=self.switch_new_entry,
        )
        new_entry_btn.pack(padx=10, pady=10, anchor="e")
        return entry_frame

    def clear_active_frame(self):
        self.default.destroy()
        self.default = Passwords(self)
        self.default.grid(row=1, column=1, sticky="news")
        if self.mainframe:
            self.mainframe.destroy()

    def switch_passwords(self):
        self.default.destroy()
        self.default = Passwords(self)
        self.default.grid(row=1, column=1, sticky="news")
        self.clear_active_frame()

    # def switch_notes(self):
    #     self.clear_active_frame()
    #     self.mainframe = Notes(self)
    #     self.mainframe.grid(row=1, column=1, sticky="news")

    def switch_generator(self):
        self.clear_active_frame()
        self.mainframe = Generator(self, self.master)
        self.mainframe.grid(row=1, column=1, sticky="news")

    def switch_settings(self):
        if self.mainframe:
            self.mainframe.destroy()
        self.mainframe = Settings(self, self.master)
        self.mainframe.grid(row=1, column=1, sticky="news")

    def switch_new_entry(self, generated_password=None):
        self.clear_active_frame()
        self.mainframe = NewEntry(
            self, parent=self.master, generated_password=generated_password
        )
        self.mainframe.grid(row=1, column=1, sticky="news")
