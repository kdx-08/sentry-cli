from pathlib import Path

import customtkinter
from PIL import Image

from sentry.generator import generate_password

copy_path = (
    Path(__file__).resolve().parent.parent.parent / "assets" / "img" / "copy.png"
)


class Generator(customtkinter.CTkFrame):
    def __init__(self, master, parent):
        super().__init__(master)
        self.label = customtkinter.CTkLabel(
            self, text="Password Generator", font=("Lexend Bold", 28)
        )
        self.pg_widget = self.generate_widget(master, parent)
        self.label.pack(padx=20, pady=10, anchor="w")
        self.pg_widget.pack(padx=20, pady=(0, 265), fill="both", expand=True)

    def generate_widget(self, master, parent):
        def update_pass_len(value):
            password_len_label.configure(text=f"No. of characters: {int(value)}")

        def copy_gen_pass():
            pg_output.clipboard_clear()
            pg_output.clipboard_append(pg_output.cget("text"))

        def gen_pass():
            is_ = False
            iu_ = False
            in_ = False
            if include_symbols.get() == "yes":
                is_ = True
            if include_uppercase.get() == "yes":
                iu_ = True
            if include_numbers.get() == "yes":
                in_ = True
            length = int(password_len.get())
            password = generate_password(length, is_, in_, iu_)
            pg_output.configure(text=password)

        pg_frame = customtkinter.CTkFrame(
            self, fg_color=("#e0e0e0", "#282828"), corner_radius=8
        )
        pg_text = customtkinter.CTkLabel(pg_frame, text="Generated password")
        pg_output_frame = customtkinter.CTkFrame(
            pg_frame, fg_color=("#ffffff", "#1e1e1e")
        )
        pg_output_frame.grid_rowconfigure(0, weight=1)
        pg_output_frame.grid_columnconfigure((0, 1), weight=1)
        pg_output = customtkinter.CTkLabel(pg_output_frame, text="")
        copy_img = customtkinter.CTkImage(
            light_image=Image.open(copy_path), dark_image=Image.open(copy_path)
        )
        copy_button = customtkinter.CTkButton(
            pg_output_frame,
            fg_color="transparent",
            text="",
            image=copy_img,
            width=48,
            hover=False,
            command=copy_gen_pass,
        )
        pg_options_frame = customtkinter.CTkFrame(
            pg_frame, fg_color="transparent", border_width=0
        )
        pg_options_frame.grid_rowconfigure((0, 1, 2), weight=1, uniform="a")
        pg_options_frame.grid_columnconfigure((0, 1), weight=1, uniform="a")
        password_len = customtkinter.CTkSlider(
            pg_options_frame,
            from_=0,
            to=40,
            number_of_steps=40,
            hover=False,
            command=update_pass_len,
            height=13,
        )
        password_len.set(16)
        password_len_label = customtkinter.CTkLabel(
            pg_options_frame, text=f"No. of characters: {int(password_len.get())}"
        )
        include_symbols = customtkinter.CTkCheckBox(
            pg_options_frame,
            text="Include symbols",
            hover=False,
            checkbox_height=16,
            checkbox_width=16,
            onvalue="yes",
            offvalue="no",
        )
        include_numbers = customtkinter.CTkCheckBox(
            pg_options_frame,
            text="Include numbers",
            hover=False,
            checkbox_width=16,
            checkbox_height=16,
            onvalue="yes",
            offvalue="no",
        )
        include_uppercase = customtkinter.CTkCheckBox(
            pg_options_frame,
            text="Include uppercase letters",
            hover=False,
            checkbox_width=16,
            checkbox_height=16,
            onvalue="yes",
            offvalue="no",
        )
        pg_btn_frame = customtkinter.CTkFrame(
            pg_frame, fg_color="transparent", border_width=0
        )
        pg_btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        copy_btn = customtkinter.CTkButton(
            pg_btn_frame,
            text="Copy to clipboard",
            hover=False,
            height=40,
            corner_radius=4,
            command=copy_gen_pass,
        )
        save_btn = customtkinter.CTkButton(
            pg_btn_frame,
            text="Save password",
            hover=False,
            height=40,
            corner_radius=4,
            text_color=("#ffffff", "#2563ec"),
            fg_color=("#2563ec", "#283d53"),
            command=lambda: master.switch_new_entry(
                generated_password=pg_output.cget("text")
            ),
        )
        gen_btn = customtkinter.CTkButton(
            pg_btn_frame,
            text="Generate password",
            hover=False,
            height=40,
            corner_radius=4,
            command=gen_pass,
        )

        pg_text.pack(padx=15, pady=(10, 0), anchor="w")
        pg_output.grid(row=0, column=0, sticky="w", ipadx=16, ipady=10)
        copy_button.grid(row=0, column=1, sticky="e")
        pg_output_frame.pack(padx=15, fill="both")
        password_len_label.grid(row=0, column=0, sticky="w", padx=15)
        password_len.grid(row=0, column=1, sticky="ew", padx=15)
        include_symbols.grid(row=1, column=0, sticky="w", padx=15, pady=12)
        include_numbers.grid(row=1, column=1, sticky="w", padx=15, pady=12)
        include_uppercase.grid(row=2, column=0, sticky="w", padx=15, pady=12)
        pg_options_frame.pack(pady=10, fill="both")
        copy_btn.grid(row=0, column=0, sticky="news", padx=(15, 5))
        save_btn.grid(row=0, column=1, sticky="news", padx=(5, 0))
        gen_btn.grid(row=0, column=3, sticky="news", padx=(0, 15))
        pg_btn_frame.pack(pady=10, fill="both")

        return pg_frame
