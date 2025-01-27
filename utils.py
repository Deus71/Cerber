import logging

DATABASE_PATH = "studniowka.db"  # lub pełna ścieżka do pliku bazy danych

#  jeśli coś pójdzie nie tak, błąd zostanie zapisany w cerber_errors.log
logging.basicConfig(filename="cerber_errors.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_error(message):
    """Zapisuje błąd do pliku logów"""
    logging.error(message)

def format_date(date):
    """Formatuje datę w standardowym formacie YYYY-MM-DD."""
    return date.strftime('%Y-%m-%d')

