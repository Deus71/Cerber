import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_participants, delete_participant
from logic import can_exit
from add_participant_gui import open_data_entry_form
from edit_participant_gui import open_edit_entry_form
from attendance_gui import register_entry_gui, register_exit_gui
from export_data import export_to_csv, export_to_pdf
from help_window import open_help_window



def open_main_window():
    window = tk.Tk()
    window.title("CERBER - Ewidencja uczestników Studniówki")
    window.geometry("1800x700")

    # Pasek menu
    menubar = tk.Menu(window)
    window.config(menu=menubar)

    program_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Program", menu=program_menu)
    program_menu.add_command(label="Zakończ", command=window.quit)

    data_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Dane", menu=data_menu)
    data_menu.add_command(label="Dodaj uczestnika", command=lambda: open_data_entry_form(window, refresh_table))
    data_menu.add_separator()
    data_menu.add_command(label="Eksportuj do CSV", command=lambda: export_to_csv("raport.csv"))
    data_menu.add_command(label="Eksportuj do PDF", command=lambda: export_to_pdf("raport.pdf"))
    
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Pomoc", menu=help_menu)
    help_menu.add_command(label="Instrukcja użytkowania", command=open_help_window)
    
    # menubar.add_cascade(label="Eksport", menu=data_menu)

    # Sekcja filtrowania (klasa + nazwisko)
    filter_frame = tk.Frame(window)
    filter_frame.pack(pady=10)

    tk.Label(filter_frame, text="Filtruj według klasy:").pack(side=tk.LEFT, padx=5)
    class_filter = ttk.Combobox(filter_frame, state="readonly", values=["Wszystkie"])
    class_filter.current(0)
    class_filter.pack(side=tk.LEFT, padx=5)

    tk.Label(filter_frame, text="Szukaj nazwiska:").pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(filter_frame)
    search_entry.pack(side=tk.LEFT, padx=5)

    # Tabela uczestników
    columns = ("ID", "Imię", "Nazwisko", "Klasa", "Wejście", "Wyjście", "Zgoda na wyjście", "Telefon rodzica", "Uwagi", "Partner - imię", "Partner - nazwisko", "Partner - klasa")

    tree = ttk.Treeview(window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    tree.pack(fill=tk.BOTH, expand=True)

    # Szczegóły uczestnika
    details_frame = tk.Frame(window)
    details_frame.pack(pady=10)

    tk.Label(details_frame, text="ID:").grid(row=0, column=0)
    selected_id = tk.Label(details_frame, text="-")
    selected_id.grid(row=0, column=1)
    
    # Przycisk edycji uczestnika
    edit_button = tk.Button(details_frame, text="Edycja danych uczestnika", command=lambda: open_edit_entry_form(window, selected_id.cget("text"), refresh_table))
    edit_button.grid(row=2, column=0, columnspan=2, pady=5)
    edit_button["state"] = "disabled"

    enter_button = tk.Button(details_frame, text="Czas wejścia", command=lambda: register_entry_gui(selected_id.cget("text"), refresh_table))
    enter_button.grid(row=1, column=0, padx=5, pady=5)

    exit_button = tk.Button(details_frame, text="Czas wyjścia", command=lambda: register_exit_gui(selected_id.cget("text"), refresh_table))
    exit_button.grid(row=1, column=1, padx=5, pady=5)
    
    delete_button = tk.Button(details_frame, text="Usuń uczestnika", command=lambda: delete_selected_participant(tree, refresh_table))
    delete_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


    enter_button["state"] = "disabled"
    exit_button["state"] = "disabled"

    def delete_selected_participant(tree, refresh_table_func):
        """Usuwa zaznaczonego uczestnika po potwierdzeniu."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Wybierz uczestnika do usunięcia!")
            return

        participant_id = tree.item(selected_item)["values"][0]  # Pobiera ID zaznaczonego uczestnika
        confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tego uczestnika?")
    
        if confirm:
            delete_participant(participant_id)
            refresh_table_func()
            messagebox.showinfo("Sukces", "Uczestnik został usunięty!")

    # Obsługa wyboru wiersza
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item)["values"]
            selected_id.config(text=values[0])
            edit_button["state"] = "normal"
            enter_button["state"] = "normal"
            exit_button["state"] = "normal"

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def refresh_table():
        """Odświeża tabelę, uwzględniając filtr klasy i wyszukiwanie po nazwisku."""
        selected_class = class_filter.get()
        search_text = search_entry.get().strip().lower()

        for row in tree.get_children():
            tree.delete(row)

        all_participants = get_all_participants()
        unique_classes = {"Wszystkie"}

        for participant in all_participants:
            unique_classes.add(participant["klasa"])

            if selected_class and selected_class != "Wszystkie" and participant["klasa"] != selected_class:
                continue

            if search_text and search_text not in participant["nazwisko"].lower():
                continue

            # Sprawdzenie zgody na wyjście
            zgoda_wyjscie = participant["zgoda_wyjscie"]
            tag = "warning" if str(participant["zgoda_wyjscie"]) not in ["1", "Tak"] else ""

            tree.insert("", tk.END, values=(
                participant["id"], participant["imie"], participant["nazwisko"],
                participant["klasa"],
                participant["czas_wejscia"] if participant["czas_wejscia"] else "-", 
                participant["czas_wyjscia"] if participant["czas_wyjscia"] else "-",
                "Tak" if str(participant["zgoda_wyjscie"]) in ["1", "Tak"] else "Nie",
                participant["telefon_rodzica"] or "-", participant["uwagi"] or "Brak",
                participant["partner_imie"] or "-", participant["partner_nazwisko"] or "-",
                participant["partner_klasa"] or "-"
            ), tags=(tag,))
            
        # Definicja stylu koloru
        tree.tag_configure("warning", background="orange")
            
        class_filter["values"] = sorted(unique_classes)
        if selected_class not in unique_classes:
            class_filter.current(0)

    search_entry.bind("<KeyRelease>", lambda event: refresh_table())
    class_filter.bind("<<ComboboxSelected>>", lambda event: refresh_table())

    refresh_table()
    window.mainloop()

