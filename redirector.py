import threading
from webbrowser import open
import sys

class Redirector:
    def redirect_to_google(self, timeout=5):

        redirect_thread = threading.Thread(target=self._redirect)
        redirect_thread.start()
        redirect_thread.join(timeout)

        if redirect_thread.is_alive():
            print("Redirection timed out. Please try again later.")
            redirect_thread.join()  # Optionally, wait for the thread to finish

    def _redirect(self):
        open('https://www.google.com')
        sys.exit()
