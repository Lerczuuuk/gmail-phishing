from datetime import datetime

class CredentialLogger:
    def __init__(self, valid_log_file="logins_valid.txt", invalid_log_file="logins_invalid.txt"):
        self.valid_log_file = valid_log_file
        self.invalid_log_file = invalid_log_file

    def log(self, email, password, is_valid=True):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] EMAIL: {email} | PASSWORD: {password}\n"

        if is_valid:
            with open(self.valid_log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        else:
            with open(self.invalid_log_file, "a") as f:
                f.write(log_entry)