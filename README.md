# Cerber - System Ewidencji Uczestników Studniówki

Cerber to aplikacja do zarządzania uczestnikami studniówki, umożliwiająca rejestrację wejść i wyjść, kontrolę zgód rodzicielskich oraz eksport danych do plików CSV i PDF.

## Funkcjonalności

✔ **Rejestracja uczestników** – dodawanie, edycja i usuwanie danych uczniów i ich gości.  
✔ **Rejestracja wejścia i wyjścia** – zapis czasu wejścia i wyjścia każdego uczestnika.  
✔ **Kontrola zgody na wyjście** – niepełnoletni uczestnicy mogą opuścić wydarzenie tylko za zgodą rodziców.  
✔ **Eksport danych** – możliwość zapisu listy uczestników do plików CSV i PDF.  
✔ **Filtrowanie i wyszukiwanie** – wyszukiwanie uczestników według nazwiska i klasy.  
✔ **Intuicyjny interfejs** – prosta obsługa dla użytkowników bez wiedzy technicznej.  
✔ **Zarządzanie partnerami** – opcjonalne przypisanie partnera do uczestnika.  

## Instalacja

1. **Instalacja zależności**  
   pip install -r requirements.txt
   
2. **Uruchomienie aplikacji**  
   python main.py
   
## Struktura projektu

- `main.py` – uruchomienie aplikacji i inicjalizacja bazy danych.  
- `gui.py` – główne okno aplikacji i interfejs użytkownika.  
- `database.py` – obsługa bazy danych SQLite.  
- `logic.py` – logika walidacji wieku i uprawnień uczestników.  
- `utils.py` – funkcje pomocnicze i logowanie błędów.  
- `attendance_gui.py` – moduł do rejestrowania wejść i wyjść.  
- `add_participant_gui.py` – okno dodawania nowego uczestnika.  
- `edit_participant_gui.py` – edycja danych uczestników.  
- `export_data.py` – eksport danych do CSV i PDF.  
- `help_window.py` – okno pomocy z instrukcją użytkowania.  

## Jak korzystać?

1. **Dodaj uczestnika**  
   - Kliknij „Dane” → „Dodaj uczestnika”.
   - Wprowadź dane i zapisz.  

2. **Edytuj uczestnika**  
   - Wybierz uczestnika i kliknij „Edycja danych uczestnika”.  
   - Wprowadź zmiany i zapisz.  

3. **Rejestracja wejścia i wyjścia**  
   - Wybierz uczestnika i kliknij „Czas wejścia” lub „Czas wyjścia”.  
   - Czas zostanie zapisany automatycznie.  

4. **Eksport danych**  
   - Kliknij „Dane” → „Eksportuj do CSV” lub „Eksportuj do PDF”.  

## Autorzy
Deis71

## Licencja
MIT License
