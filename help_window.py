import tkinter as tk
from tkinter import scrolledtext

def open_help_window():
    """Tworzy okno pomocy z instrukcjami użytkowania aplikacji."""
    help_window = tk.Toplevel()
    help_window.title("Pomoc - Instrukcja użytkowania")
    help_window.geometry("600x500")
    
    instructions = """
    *** Instrukcja użytkowania ***

    1. **Dodawanie uczestnika:**
       - Kliknij "Dane" -> "Dodaj uczestnika".
       - Wypełnij wymagane pola.
       - Kliknij "Zapisz", aby dodać uczestnika do bazy.
    
    2. **Edycja danych uczestnika:**
       - Wybierz uczestnika z listy.
       - Kliknij "Edytowanie danych uczestnika".
       - Zmień dane i kliknij "Zapisz zmiany".
    
    3. **Rejestracja wejścia i wyjścia:**
       - Wybierz uczestnika z listy.
       - Kliknij "Rejestruj wejście", aby zapisać godzinę wejścia.
       - Kliknij "Rejestruj wyjście", aby zapisać godzinę wyjścia.
    
    4. **Filtrowanie i wyszukiwanie:**
       - Aby filtrować uczestników według klasy, wybierz klasę z listy.
       - Aby wyszukać uczestnika, wpisz jego nazwisko w polu wyszukiwania.
    
    5. **Eksport danych:**
       - Kliknij "Dane" -> "Eksportuj do CSV", aby zapisać dane w pliku CSV.
       - Kliknij "Dane" -> "Eksportuj do PDF", aby zapisać dane w pliku PDF.
       - Pliki zostaną zapisane w katalogu programu.
    
    *** W razie problemów skontaktuj się z administratorem systemu. ***
    """
    
    text_area = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, width=70, height=25)
    text_area.insert(tk.INSERT, instructions)
    text_area.config(state=tk.DISABLED)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    close_button = tk.Button(help_window, text="Zamknij", command=help_window.destroy)
    close_button.pack(pady=10)
    
    help_window.mainloop()

