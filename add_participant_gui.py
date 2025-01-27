import tkinter as tk
from tkinter import messagebox, ttk
from database import add_participant

def open_data_entry_form(parent, refresh_table_func):
    """Otwiera okno dodawania nowego uczestnika."""
    top = tk.Toplevel(parent)
    top.title("Dodaj uczestnika")

    # Mapowanie nazw pól GUI na kolumny w bazie danych
    field_labels = {
        "Imię:": "imie",
        "Nazwisko:": "nazwisko",
        "Klasa:": "klasa",
        "Zgoda na wyjście:": "zgoda_wyjscie",
        "Telefon rodzica/opiekuna:": "telefon_rodzica",
        "Dodatkowe uwagi:": "uwagi",
        "Imię partnera:": "partner_imie",
        "Nazwisko partnera:": "partner_nazwisko",
        "Klasa partnera:": "partner_klasa"
    }

    # Opcje do wyboru dla pól :Klasa", "Status ucznia" i "Zgoda na wyjście"
    klasa_options = ["4A", "4B", "4D1", "4D2", "4F", "Gość"]
    zgoda_wyjscie_options = ["Tak", "Nie"]
    partner_klasa_options = ["4A", "4B", "4D1", "4D2", "4F", "Gość"]

    entries = {}
    for i, (label, field) in enumerate(field_labels.items()):
        tk.Label(top, text=label).grid(row=i, column=0, sticky="e")

        if field == "klasa":
            entry = ttk.Combobox(top, values=klasa_options, state="readonly")
            entry.current()  # Domyślnie puste
        elif field == "zgoda_wyjscie":
            entry = ttk.Combobox(top, values=zgoda_wyjscie_options, state="readonly")
            entry.current(1)  # Domyślnie "Nie"
        elif field == "partner_klasa":
            entry = ttk.Combobox(top, values=partner_klasa_options, state="readonly")
            entry.current()  # Domyślnie puste
        else:
            entry = tk.Entry(top)

        entry.grid(row=i, column=1, sticky="we")
        entries[field] = entry  # Przechowujemy pola jako klucze z bazy danych

    def save_participant():
        """Zapisuje nowego uczestnika do bazy."""
        try:
            participant_data = {field: entry.get() for field, entry in entries.items()}
            add_participant(**participant_data)
            messagebox.showinfo("Sukces", "Uczestnik został dodany!")
            refresh_table_func()
            top.destroy()
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się dodać uczestnika: {e}")
            
    def show_help():
        """Wyświetla okno pomocy z instrukcjami dotyczącymi wypełniania pól."""
        help_window = tk.Toplevel(top)
        help_window.title("Instrukcja wypełniania formularza")
        help_text = """\
    Instrukcja wypełniania:

    - Imię i Nazwisko: Wprowadź pełne imię i nazwisko uczestnika.
    - Klasa: Wybierz klasę ucznia (np. 4A) lub „Gość” dla osoby spoza szkoły.
    - Zgoda na samodzielne wyjście: Jeśli uczestnik jest niepełnoletni, wymagana jest zgoda rodzica. 
      Wybierz „Tak” jeżeli rodzic wyraził zgodę lub „Nie” jeżeli jej brak.
    - Telefon rodzica/opiekuna: Wpisz numer telefonu w formacie 123 456 789.
    - Uwagi: Możesz dodać dowolne informacje (np. alergie).
    - Dane partnera: Opcjonalnie wpisz dane partnera (jeśli dotyczy).

    Kliknij „Dodaj”, aby zapisać uczestnika. 
    Kliknij "Anuluj", aby porzucić dodawanie uczestnika.
    """
        label = tk.Label(help_window, text=help_text, justify="left", padx=10, pady=20)
        label.pack()

        close_button = tk.Button(help_window, text="Zamknij", command=help_window.destroy)
        close_button.pack(pady=5)
    
    # Dodanie przycisku Pomoc
    tk.Button(top, text="Pomoc", command=show_help).grid(row=len(field_labels), column=2, sticky="we")
    # Dodanie przycisku Dodaj
    tk.Button(top, text="Dodaj", command=save_participant).grid(row=len(field_labels), column=1, sticky="we")
    # Dodanie przycisku Anuluj
    tk.Button(top, text="Anuluj", command=top.destroy).grid(row=len(field_labels) + 1, column=1, sticky="we")

    top.grid_columnconfigure(1, weight=1)

