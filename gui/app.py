import customtkinter

from gui.screens.dashboard_screen import Dashboard
from gui.screens.login_screen import Login
from sentry.parser import read_config

customtkinter.set_default_color_theme("gui/assets/theme/theme.json")
customtkinter.set_appearance_mode(read_config("appearance"))
customtkinter.FontManager().load_font("gui/assets/fonts/Lexend-VariableFont.ttf")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sentry")
        self.geometry("960x720")
        self.iconbitmap("gui/assets/img/sentry-ico.ico")
        self.resizable(False, False)

        self.username = read_config("username")
        self.theme = customtkinter.StringVar(value=read_config("appearance"))
        self.db_path = read_config("db_path")
        self.current_screen = None
        self.master_password = ""
        self.login_screen()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    def dashboard_screen(self):
        self.clear_screen()
        self.current_screen = Dashboard(self)
        self.current_screen.pack(fill="both", expand=True)

    def login_screen(self):
        self.clear_screen()
        self.current_screen = Login(self)
        self.current_screen.pack(fill="both", expand=True)


if __name__ == "__main__":
    App().mainloop()
