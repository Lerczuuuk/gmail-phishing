# Gmail Phishing Simulator

## About

A learning project that simulates a Gmail login form with features like:
- Email and password validation.
- Logging successful and failed login attempts.
- OTP (One-Time Password) verification.
- Redirection to the actual Gmail website.

## Requirements

- **Python 3.10+**
- Install dependencies with:
  ```bash
  pip install pillow customtkinter
  ```

## How to Run

1. Place all files (e.g., `main.py`, `Google.png`) in one folder.
2. Run:
   ```bash
   python main.py
   ```
3. Enter email/password in the GUI, and logs will be saved in:
   - `logins.valid.txt`
   - `logins.invalid.txt`

## Features

- Email format and password strength validation.
- OTP generation and verification.
- Redirection via a web browser.
- Simple logging system for attempts.

## Notes

This project is for practice purposes only and not intended for real phishing activities.

## Author

Created for Python learning purposes. Feel free to use this project in your own learning.

---
