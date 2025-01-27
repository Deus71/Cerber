import sys
from gui import open_main_window
from database import initialize_database

def main():
    # Inicjalizacja bazy danych
    initialize_database()

    # Uruchomienie interfejsu graficznego
    open_main_window()

if __name__ == "__main__":
    main()

