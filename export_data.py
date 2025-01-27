import csv
import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from database import get_all_participants
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Pobranie ścieżki katalogu projektu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "fonts")

# Rejestracja czcionek z lokalnego folderu projektu
pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(FONT_PATH, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(FONT_PATH, "DejaVuSans-Bold.ttf")))

def export_to_csv(filename="raport.csv"):
    """Eksportuje dane uczestników do pliku CSV."""
    participants = get_all_participants()
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Imię", "Nazwisko", "Klasa", "Wejście", "Wyjście",
                         "Zgoda", "Telefon", "Uwagi", "Partner"])
        
        for participant in participants:
            writer.writerow([
                participant["id"], participant["imie"], 
                participant["nazwisko"], participant["klasa"] or "Nieznana klasa",
                participant.get("czas_wejscia", "-"),
                participant.get("czas_wyjscia", "-"),
                "Tak" if str(participant["zgoda_wyjscie"]) in ["1", "Tak"] else "Nie",
                participant["telefon_rodzica"] or "-", participant["uwagi"] or "-",
                f"{participant['partner_imie'] or '-'} {participant['partner_nazwisko'] or '-'} ({participant['partner_klasa'] or '-'})"
            ])
    print(f"Dane zapisano do {filename}")

def export_to_pdf(filename="raport.pdf"):
    """Eksportuje dane uczestników do pliku PDF, grupując ich według klasy."""
    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("DejaVu", 12)
    participants = get_all_participants()
    grouped_by_class = {}

    for participant in participants:
        klasa = participant["klasa"] or "Nieznana klasa"
        if klasa not in grouped_by_class:
            grouped_by_class[klasa] = []
        grouped_by_class[klasa].append(participant)
    
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    elements = []
    
    for klasa, students in sorted(grouped_by_class.items()):
        if not students:
            continue  # Pomijamy puste klasy
        
        elements.append(Table([[f"Klasa: {klasa}"]], colWidths=750))
        elements.append(Spacer(1, 10))
        data = [["ID", "Imię", "Nazwisko", "Wejście", "Wyjście", "Zgoda", "Telefon", "Uwagi", "Partner"]]
        
        for participant in students:
            data.append([
                participant["id"], participant["imie"], participant["nazwisko"], 
                participant.get("czas_wejscia", "-"), participant.get("czas_wyjscia", "-"),
                "Tak" if str(participant["zgoda_wyjscie"]) in ["1", "Tak"] else "Nie",
                participant["telefon_rodzica"] or "-", participant["uwagi"] or "-",
                f"{participant['partner_imie'] or '-'} {participant['partner_nazwisko'] or '-'} ({participant['partner_klasa'] or '-'})"
            ])
        
        table = Table(data, colWidths=[30, 80, 80, 60, 60, 50, 70, 90, 120])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVu-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 1), (-1, -1), 'DejaVu')
        ]))
        elements.append(table)
        elements.append(Spacer(1, 15))
    
    doc.build(elements)
    print(f"Dane zapisano do {filename}")

