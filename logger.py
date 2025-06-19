from datetime import datetime


class BaseLogger: #dziedziczenie
    def log(self, email: str, password: str, is_valid: bool):
        raise NotImplementedError("You must override the log() method in the class.")


class CredentialLogger(BaseLogger):
    def __init__(self, valid_log_file='valid_credentials.txt', invalid_log_file='invalid_credentials.txt'):
        self.valid_log_file = valid_log_file
        self.invalid_log_file = invalid_log_file

    def log(self, email: str, password: str, is_valid: bool):
        log_file = self.valid_log_file if is_valid else self.invalid_log_file
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | {email} | {password}\n"

        with open(log_file, 'a', encoding='utf-8') as file:
            file.write(log_entry)