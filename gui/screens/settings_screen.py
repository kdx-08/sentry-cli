import customtkinter


class Settings(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = customtkinter.CTkLabel(self, text="Settings")
        self.label.pack(padx=10, pady=10)
