import sqlite3
from datetime import datetime
from utils import DATABASE_PATH

DATABASE_PATH = 'studniowka.db'

def register_entry(participant_id):
    """Zapisuje czas wejścia uczestnika."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime('%H:%M')
    cursor.execute("UPDATE uczestnicy SET czas_wejscia = ? WHERE id = ?", (now, participant_id))
    conn.commit()
    conn.close()

def register_exit(participant_id):
    """Zapisuje czas wyjścia uczestnika."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime('%H:%M')
    cursor.execute("UPDATE uczestnicy SET czas_wyjscia = ? WHERE id = ?", (now, participant_id))
    conn.commit()
    conn.close()
    
def delete_participant(participant_id):
    """Usuwa uczestnika z bazy danych na podstawie ID."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM uczestnicy WHERE id = ?", (participant_id,))
    conn.commit()
    conn.close()

def initialize_database():
    """Tworzy tabelę uczestników, jeśli nie istnieje."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uczestnicy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imie TEXT,
            nazwisko TEXT,
            klasa TEXT,
            czas_wejscia TEXT,
            czas_wyjscia TEXT,
            zgoda_wyjscie BOOLEAN,
            telefon_rodzica TEXT,
            uwagi TEXT,
            partner_imie TEXT,
            partner_nazwisko TEXT,
            partner_klasa TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_participant(imie, nazwisko, klasa, zgoda_wyjscie, telefon_rodzica, uwagi, partner_imie, partner_nazwisko, partner_klasa):
    """Dodaje nowego uczestnika do bazy."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO uczestnicy (imie, nazwisko, klasa, zgoda_wyjscie, telefon_rodzica, uwagi, partner_imie, partner_nazwisko, partner_klasa)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (imie, nazwisko, klasa, zgoda_wyjscie, telefon_rodzica, uwagi, partner_imie, partner_nazwisko, partner_klasa))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Błąd podczas dodawania uczestnika: {e}")
        messagebox.showerror("Błąd", "Nie udało się dodać uczestnika.") 

def get_all_participants():
    """Zwraca listę wszystkich uczestników."""
    try: 
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, imie, nazwisko, klasa, czas_wejscia, czas_wyjscia, zgoda_wyjscie, uwagi, telefon_rodzica, partner_imie, partner_nazwisko, partner_klasa
            FROM uczestnicy
        ''')
        participants = [{column[0]: row[i] for i, column in enumerate(cursor.description)} for row in cursor.fetchall()]
        conn.close()
        return participants
    except sqlite3.Error as e:
        logging.error(f"Błąd podczas pobierania uczestników: {e}")
        messagebox.showerror("Błąd bazy danych", "Nie udało się pobrać listy uczestników.")
        return []

def get_participant_by_id(participant_id):
    """Pobiera dane konkretnego uczestnika na podstawie jego ID."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, imie, nazwisko, klasa, czas_wejscia, czas_wyjscia, zgoda_wyjscie, telefon_rodzica, uwagi, partner_imie, partner_nazwisko, partner_klasa
        FROM uczestnicy WHERE id = ?
    ''', (participant_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0], "imie": row[1], "nazwisko": row[2], "klasa": row[3], "czas_wejscia": row[4], "czas_wyjscia": row[5], "zgoda_wyjscie": row[6], "telefon_rodzica": row[7], "uwagi": row[8], "partner_imie": row[9], "partner_nazwisko": row[10], "partner_klasa": row[11]
        }
    return None

def update_participant(participant_id, imie, nazwisko, klasa, zgoda_wyjscie, telefon_rodzica, uwagi, partner_imie, partner_nazwisko, partner_klasa):
    """Aktualizuje dane uczestnika na podstawie jego ID."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE uczestnicy SET
        imie = ?, nazwisko = ?, klasa = ?, zgoda_wyjscie = ?, telefon_rodzica = ?, uwagi = ?, partner_imie = ?, partner_nazwisko = ?, partner_klasa = ?
        WHERE id = ?
    ''', (imie, nazwisko, klasa, zgoda_wyjscie, telefon_rodzica, uwagi, partner_imie, partner_nazwisko, partner_klasa, participant_id))
    conn.commit()
    conn.close()

