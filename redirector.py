import webbrowser
import sys

class Redirector:
    def redirect_to_google(self):
        webbrowser.open('https://www.google.com')
        sys.exit()