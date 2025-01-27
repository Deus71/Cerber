import tkinter as tk
from tkinter import messagebox, ttk
import logging
from database import update_participant, get_participant_by_id

# Konfiguracja logowania
logging.basicConfig(filename="cerber_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def open_edit_entry_form(parent, participant_id, refresh_table_func):
    """Otwiera formularz do edycji danych uczestnika."""
    top = tk.Toplevel(parent)
    top.title("Edytowanie uczestnika")

    participant = get_participant_by_id(participant_id)
    if not participant:
        messagebox.showerror("Błąd", "Nie znaleziono uczestnika.")
        return

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
            entry.set(participant.get(field, ""))  # Pobranie wartości z bazy
        elif field == "zgoda_wyjscie":
            # Konwersja wartości z bazy (1 -> "Tak", 0 -> "Nie")
            current_value = "Tak" if str(participant.get(field, "Nie")) in ["1", "Tak"] else "Nie"
            entry = ttk.Combobox(top, values=zgoda_wyjscie_options, state="readonly")
            entry.set(current_value)  # Pobranie wartości z bazy
        elif field == "partner_klasa":
            entry = ttk.Combobox(top, values=partner_klasa_options, state="readonly")
            entry.set(participant.get(field, ""))  # Pobranie wartości z bazy
        else:
            entry = tk.Entry(top)
            entry.insert(0, participant.get(field, ""))

        entry.grid(row=i, column=1, sticky="we")
        entries[field] = entry

    def save_changes():
        """Zapisuje zmiany w danych uczestnika."""
        try:
            updated_data = {field: entry.get() for field, entry in entries.items()}
            update_participant(participant_id, **updated_data)
            messagebox.showinfo("Sukces", "Dane uczestnika zostały zaktualizowane!")
            refresh_table_func()
            top.destroy()
        except Exception as e:
            logging.error(f"Błąd podczas edytowania uczestnika {participant_id}: {e}")
            messagebox.showerror("Błąd", "Nie udało się zaktualizować danych uczestnika.")

    def show_help():
        """Wyświetla okno pomocy z instrukcjami dotyczącymi wypełniania pól."""
        help_window = tk.Toplevel(top)
        help_window.title("Pomoc")
        help_text = """\
    Instrukcja wypełniania:

    - Imię i Nazwisko: Wprowadź pełne imię i nazwisko uczestnika.
    - Klasa: Wybierz klasę ucznia (np. 4A) lub „Gość” dla osoby spoza szkoły.
    - Zgoda na samodzielne wyjście: Jeśli uczestnik jest niepełnoletni, wymagana jest zgoda rodzica. 
      Wpisz Tak jeżeli rodzic wyraził zgodę lub Nie jeżeli jej brak.
    - Telefon rodzica/opiekuna: Wpisz numer telefonu w formacie 123 456 789.
    - Uwagi: Możesz dodać dowolne informacje (np. alergie).
    - Dane partnera: Opcjonalnie wpisz dane partnera (jeśli dotyczy).

    Kliknij „Zapisz zmiany”, aby zapisać uczestnika. 
    Kliknij "Anuluj", aby porzucić edycję uczestnika.
    """
        label = tk.Label(help_window, text=help_text, justify="left", padx=10, pady=10)
        label.pack()

        close_button = tk.Button(help_window, text="Zamknij", command=help_window.destroy)
        close_button.pack(pady=5)
    
    # Dodanie przycisku Pomoc
    tk.Button(top, text="Pomoc", command=show_help).grid(row=len(field_labels), column=2, sticky="we")
    # Dodanie przycisku Zapisz    
    tk.Button(top, text="Zapisz zmiany", command=save_changes).grid(row=len(field_labels), column=1, sticky="we")
    # Dodanie przycisku Anuluj    
    tk.Button(top, text="Anuluj", command=top.destroy).grid(row=len(field_labels) + 1, column=1, sticky="we")

    top.grid_columnconfigure(1, weight=1)

