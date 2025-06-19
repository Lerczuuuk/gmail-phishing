import threading
from webbrowser import open as open_browser
import sys
from abc import ABC, abstractmethod


class BaseRedirector(ABC):
    #Klasa bazowa z metodą abstrakcyjną do nadpisania
    @abstractmethod
    def _redirect(self, url: str):
        pass


class Redirector(BaseRedirector):
    def __init__(self):
        self._redirect_count = 0

    # NADPISYWANIE METODY
    def _redirect(self, url: str): #metoda prywatna
        print(f"[LOG] Próba przekierowania do: {url}")
        try:
            open_browser(url)
            self._redirect_count += 1
            print("[LOG] Przekierowanie udane")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Błąd przekierowania: {e}")
            sys.exit(1)

    def redirect_to_google(self, timeout=5):
        #Metoda publicza wykorzystująca nadpisaną _redirect
        print(f"Rozpoczynanie przekierowania (timeout: {timeout}s)...")

        thread = threading.Thread(target=self._redirect, args=('https://www.google.com',))
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            print("Przekroczono czas oczekiwania na przekierowanie")
            thread.join()

    # Przeciążone operatory (pozostałe metody)
    def __str__(self):
        return f"Redirector (licznik: {self._redirect_count})"

    def __len__(self):
        return self._redirect_count

    def __add__(self, other):
        if not isinstance(other, Redirector):
            raise TypeError("Można łączyć tylko z innym Redirector")
        new_obj = Redirector()
        new_obj._redirect_count = self._redirect_count + other._redirect_count
        return new_obj