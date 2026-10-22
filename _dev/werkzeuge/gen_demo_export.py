#!/usr/bin/env python3
# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Fictitious Papierkram exports of a small photo studio, to try the import.

Writes into OUTPUT_DIR (default ``build/demo``):

- ``export_fotostudio_muster_papierkram_<year>.zip`` for 2024 and 2025 in the
  layout of a Papierkram export *Vollständig (CSV, PDF)* (CSV files only);
- ``kategorien.csv``: the categories with their SKR03 accounts;
- ``anlagegueter.csv``: the fixed assets as exported under *Ausgaben →
  Anlagegüter*.

All names, numbers and amounts are invented. The business is a small business
(§ 19 UStG): invoices without VAT, vouchers with their gross amounts.

Usage::

    python3 -I _dev/werkzeuge/gen_demo_export.py [OUTPUT_DIR]
"""

# pylint: disable=print-used

import os
import sys
import zipfile

H_RECHNUNGEN = (
    "Rechnungsnr.;Betreff;Kunde;Land;Projekt;Kundennummer;Datum;Fälligkeitsdatum;"
    "Status;Typ;Netto;USt.;Brutto;Skonto;Bezahlt;letztes Bezahldatum;Notiz;"
    "Mahnungsdatum;Waren & Dienstleistungen"
)
H_BELEGE = (
    "Belegnummer;Gegenstand;Lieferant;Datum;Zahlungsfrist;Zahlung am;Status;Netto;"
    "USt.;Brutto;Privatanteil;Herkunftsort;Kategorien;Projekte;Projektkunden;"
    "Projektkunden-Nr;Zusatz;Notizen"
)
H_ZAHLUNGEN = "Buchung;Kundennummer;Rechnungsnummer;Belegnummer;Datum;Betrag"
H_KONTAKTE = (
    "Name;Kontaktart;Kunden-/Lieferantennr.;Straße (Post);PLZ (Post);Stadt (Post);"
    "Land (Post);Straße (Haus);PLZ (Haus);Stadt (Haus);Land;Website;E-Mail;Telefon;"
    "Fax;UStID;Notiz;Kontonummer;Bankname;BLZ;IBAN;BIC;SEPA-Mandatsreferenz;"
    "SEPA-Lastschrift akzeptiert;Anrede (Standardempfänger);Titel (Standardempfänger);"
    "Vorname (Standardempfänger);Nachname (Standardempfänger);"
    "E-Mail (Standardempfänger);Telefonnummer (Standardempfänger);"
    "Fax (Standardempfänger);Handynummer (Standardempfänger);"
    "Skype (Standardempfänger);Notiz (Standardempfänger)"
)
H_KONTOUMSAETZE = (
    "Status;Zahlungswert;Zahlungswährung;Storniert;Kunden-Referenz;Instref;GV-Code;"
    "Kategorie;Verwendungszweck;Primanota;SEPA?;Absender-IBAN;Absender-BIC;"
    "Absender-Kontonummer;Absender-BLZ;Absender-Währung;Absender-Name;Saldo-Wert;"
    "Saldo-Währung;Saldo-Zeitpunkt;Bankverbindung-ID;Valuta;Buchungsdatum;"
    "Importierungsdatum"
)
KATEGORIEN = (
    "name;skr03;konto_name;konto_typ;abschreibungsart;typ\n"
    "Porto;4910;Porto;EXPENSE;;EXPENSE\n"
    "Bürobedarf;4930;Bürobedarf;EXPENSE;;EXPENSE\n"
    "Werkzeuge und Kleingeräte;4985;Werkzeuge und Kleingeräte;EXPENSE;;EXPENSE\n"
    "Zeitschriften, Bücher;4940;Zeitschriften, Bücher;EXPENSE;;EXPENSE\n"
    "Werbekosten;4600;Werbekosten;EXPENSE;;EXPENSE\n"
    "Sonstige betriebliche Aufwendungen;4900;Sonstige;EXPENSE;;EXPENSE\n"
    "Betriebsausstattung (Anlage);400;Betriebsausstattung;NEUTRAL;AFA;ASSET\n"
)
#: the camera: 2,100.00 € on 05.02.2024, 7 years (25.00 € per month)
ANLAGEGUETER = (
    "Belegnummer;Beleg;Restwert Jahresende;Anschaffungsdatum;Anschaffungswert;"
    "monatl. Abschreibung\n"
    "B-00001;Systemkamera mit Objektiv;1.825,00;05.02.2024;2.100,00;25,00\n"
)

#: number, name, kind, country (postal)
KONTAKTE = (
    ("K-00001", "Muster GmbH", "Kunde", "Deutschland"),
    ("K-00002", "Lea und Tom Beispiel", "Kunde", "Deutschland"),
    ("K-00003", "Café am Markt Beispiel", "Kunde", "Deutschland"),
    ("K-00004", "Kulturverein Musterstadt e. V.", "Kunde", "Deutschland"),
    ("L-00001", "Kamerahaus Beispiel GmbH", "Lieferant", "Deutschland"),
    ("L-00002", "Druckerei Muster", "Lieferant", "Deutschland"),
    ("L-00003", "Serverdienst Beispiel AG", "Lieferant", "Deutschland"),
    ("L-00004", "Post und Paket Muster", "Lieferant", "Deutschland"),
)
CUSTOMERS = {name: number for number, name, kind, _c in KONTAKTE if kind == "Kunde"}

#: invoices: number, subject, customer, date, due date, amount, paid on (or "")
RECHNUNGEN = {
    2024: (
        (
            "R-00001",
            "Firmenportraits",
            "Muster GmbH",
            "12.03.2024",
            "26.03.2024",
            "450,00",
            "2024-03-20",
        ),
        (
            "R-00002",
            "Paarshooting am See",
            "Lea und Tom Beispiel",
            "08.06.2024",
            "22.06.2024",
            "620,00",
            "2024-06-18",
        ),
        (
            "R-00003",
            "Speisekartenfotos",
            "Café am Markt Beispiel",
            "02.09.2024",
            "16.09.2024",
            "320,00",
            "2024-09-10",
        ),
        (
            "R-00004",
            "Online-Galerie 2025",
            "Kulturverein Musterstadt e. V.",
            "16.12.2024",
            "30.12.2024",
            "150,00",
            "2024-12-29",
        ),
    ),
    2025: (
        (
            "R-00005",
            "Abteilungsfotos Vertrieb",
            "Muster GmbH",
            "18.02.2025",
            "04.03.2025",
            "680,00",
            "2025-02-27",
        ),
        (
            "R-00006",
            "Produktfotos Frühjahrskarte",
            "Café am Markt Beispiel",
            "07.04.2025",
            "21.04.2025",
            "290,00",
            "2025-04-16",
        ),
        (
            "R-00007",
            "Porträts im Atelier",
            "Lea und Tom Beispiel",
            "15.05.2025",
            "29.05.2025",
            "240,00",
            "2025-05-26",
        ),
        (
            "R-00008",
            "Vereinsfotos Jahreskonzert",
            "Kulturverein Musterstadt e. V.",
            "01.08.2025",
            "15.08.2025",
            "350,00",
            "2025-08-12",
        ),
        (
            "R-00009",
            "Firmenjubiläum",
            "Muster GmbH",
            "20.10.2025",
            "03.11.2025",
            "1.150,00",
            "2025-10-31",
        ),
        (
            "R-00010",
            "Online-Galerie 2026",
            "Kulturverein Musterstadt e. V.",
            "15.12.2025",
            "29.12.2025",
            "150,00",
            "",
        ),
    ),
}

#: vouchers: number, subject, supplier, date, gross amount, category
BELEGE = {
    2024: (
        (
            "B-00001",
            "Systemkamera mit Objektiv",
            "Kamerahaus Beispiel GmbH",
            "05.02.2024",
            "2.100,00",
            "Betriebsausstattung (Anlage)",
        ),
        (
            "B-00002",
            "Speicherkarten und Akku",
            "Kamerahaus Beispiel GmbH",
            "05.02.2024",
            "129,90",
            "Werkzeuge und Kleingeräte",
        ),
        (
            "B-00003",
            "Visitenkarten",
            "Druckerei Muster",
            "20.03.2024",
            "49,00",
            "Werbekosten",
        ),
        (
            "B-00004",
            "Galerie-Server 2024",
            "Serverdienst Beispiel AG",
            "02.01.2024",
            "96,00",
            "Sonstige betriebliche Aufwendungen",
        ),
        (
            "B-00005",
            "Versand Album",
            "Post und Paket Muster",
            "11.06.2024",
            "6,99",
            "Porto",
        ),
    ),
    2025: (
        (
            "B-00006",
            "Galerie-Server 2025",
            "Serverdienst Beispiel AG",
            "02.01.2025",
            "96,00",
            "Sonstige betriebliche Aufwendungen",
        ),
        (
            "B-00007",
            "Albumdruck",
            "Druckerei Muster",
            "12.05.2025",
            "112,40",
            "Sonstige betriebliche Aufwendungen",
        ),
        (
            "B-00008",
            "Versand Album",
            "Post und Paket Muster",
            "26.05.2025",
            "6,99",
            "Porto",
        ),
        (
            "B-00009",
            "Studiohintergrund",
            "Kamerahaus Beispiel GmbH",
            "14.07.2025",
            "189,00",
            "Werkzeuge und Kleingeräte",
        ),
        (
            "B-00010",
            "Fachbuch Bildgestaltung",
            "Kamerahaus Beispiel GmbH",
            "03.09.2025",
            "42,80",
            "Zeitschriften, Bücher",
        ),
        (
            "B-00011",
            "Druckerpapier und Toner",
            "Druckerei Muster",
            "17.11.2025",
            "84,50",
            "Bürobedarf",
        ),
    ),
}


def contact_row(number, name, kind, country):
    cells = [name, kind, number, "", "", "", country] + [""] * 27
    return ";".join(cells)


def invoice_row(number, subject, customer, date, due, amount, paid_on):
    state = "Bezahlt" if paid_on else "Unbezahlt"
    paid = amount if paid_on else "0,00"
    cells = (
        number,
        subject,
        customer,
        "Deutschland",
        "",
        CUSTOMERS[customer],
        date,
        due,
        state,
        "Rechnung",
        amount,
        "0,00",
        amount,
        "0,00",
        paid,
        paid_on,
        "",
        "",
        "",
    )
    return ";".join(cells)


def voucher_row(number, subject, supplier, date, gross, category):
    day, month, year = date.split(".")
    iso = f"{year}-{month}-{day}"
    cells = (
        number,
        subject,
        supplier,
        date,
        "",
        iso,
        "paid",
        f"-{gross}",
        "0,00",
        f"-{gross}",
        "0",
        "domestic",
        category,
        "",
        "",
        "",
        "",
        "",
    )
    return ";".join(cells)


def payments(year):
    rows = []
    for number, _s, customer, _d, _due, amount, paid_on in RECHNUNGEN[year]:
        if paid_on:
            customer_number = CUSTOMERS[customer]
            rows.append(
                f"Zahlung zu {number};{customer_number};{number};;{paid_on};{amount}"
            )
    for number, _s, _sup, date, gross, _c in BELEGE[year]:
        day, month, yyyy = date.split(".")
        rows.append(f"Zahlung zu {number};;;{number};{yyyy}-{month}-{day};-{gross}")
    return rows


def write(directory):
    os.makedirs(directory, exist_ok=True)
    paths = []
    for year in sorted(RECHNUNGEN):
        path = os.path.join(
            directory, f"export_fotostudio_muster_papierkram_{year}.zip"
        )
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr(
                "CSV/Rechnungen.csv",
                "\n".join((H_RECHNUNGEN, *(invoice_row(*r) for r in RECHNUNGEN[year])))
                + "\n",
            )
            zf.writestr(
                "CSV/Belege.csv",
                "\n".join((H_BELEGE, *(voucher_row(*b) for b in BELEGE[year]))) + "\n",
            )
            zf.writestr(
                "CSV/Zahlungseingänge.csv",
                "\n".join((H_ZAHLUNGEN, *payments(year))) + "\n",
            )
            zf.writestr(
                "CSV/Kontakte.csv",
                "\n".join((H_KONTAKTE, *(contact_row(*k) for k in KONTAKTE))) + "\n",
            )
            zf.writestr("CSV/Kontoumsätze.csv", H_KONTOUMSAETZE + "\n")
        paths.append(path)
    for name, content in (
        ("kategorien.csv", KATEGORIEN),
        ("anlagegueter.csv", ANLAGEGUETER),
    ):
        path = os.path.join(directory, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        paths.append(path)
    return paths


def main(argv):
    directory = argv[1] if len(argv) > 1 else os.path.join("build", "demo")
    for path in write(directory):
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
