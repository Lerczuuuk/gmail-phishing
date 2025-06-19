from gui import PhishingGUI

def main():
    try:
        app = PhishingGUI()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()