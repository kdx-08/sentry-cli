import customtkinter
import sys
from sentry.vault.vault_manager import reset_app_data

def reset_sentry_application(reset_desc):
  reset_dialog = customtkinter.CTkInputDialog(title="Reset Sentry", text="Are you sure you want to reset Sentry? This will permanently erase all encrypted passwords, secure notes, and stored application data from this device. This action cannot be undone. Enter \"RESET SENTRY\" to proceed.")

  screen_width = reset_dialog.winfo_screenwidth()
  screen_height = reset_dialog.winfo_screenheight()
  x = (screen_width // 2) - (360 // 2)
  y = (screen_height // 2) - (240 // 2)
  reset_dialog.geometry(f"{360}x{240}+{x}+{y}")

  choice = reset_dialog.get_input()
  if choice is not None and choice == "RESET SENTRY":
    reset_desc.configure(text="Sentry will be reset.",  text_color="green")
    reset_app_data()
    sys.exit(0)
  else:
    reset_desc.configure(text="Reset cancelled.",  text_color="red")
