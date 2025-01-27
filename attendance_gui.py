import tkinter as tk
from tkinter import messagebox
from database import register_entry, register_exit

def register_entry_gui(participant_id, refresh_table_func):
    """Rejestruje wejście uczestnika i aktualizuje tabelę."""
    if not participant_id or participant_id == "-":
        messagebox.showerror("Błąd", "Nie wybrano uczestnika.")
        return
    
    try: 
        register_entry(participant_id)
        messagebox.showinfo("Sukces", "Wejście zostało zarejestrowane!")
        refresh_table_func()
    except Exception as e:
        logging.error(f"Błąd przy rejestrowaniu wejścia: {e}")
        messagebox.showerror("Błąd", "Nie udało się zarejestrować wejścia uczestnika.")

def register_exit_gui(participant_id, refresh_table_func):
    """Rejestruje wyjście uczestnika i aktualizuje tabelę."""
    if not participant_id or participant_id == "-":
        messagebox.showerror("Błąd", "Nie wybrano uczestnika.")
        return
    
    try: 
        register_exit(participant_id)
        messagebox.showinfo("Sukces", "Wyjście zostało zarejestrowane!")
        refresh_table_func()
    except Exception as e:
        logging.error(f"Błąd przy rejestrowaniu wyjścia: {e}")
        messagebox.showerror("Błąd", "Nie udało się zarejestrować wyjścia uczestnika.")

