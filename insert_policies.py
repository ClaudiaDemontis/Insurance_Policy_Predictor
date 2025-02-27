# --- INSERT POLICIES ---

# Imports
import csv
from faker import Faker
import mysql.connector
from mysql.connector import Error
from funzioni_utili import esegui_query
from funzioni_utili import esegui_query_parametrizzata
import datetime

# Inserimento dei dati nella tabella

# lettura del csv
with open("Insurance_cleaned.csv", encoding="utf-8") as f:
    dati = csv.reader(f)
    next(dati)

    fake = Faker()

    # creo una lista vuota policies
    policies = []

    # associo le righe del csv ai campi delle tabelle
    for riga in dati:
        age = riga[0]
        sex = riga[1]
        bmi = riga[2]
        children = riga[3]
        smoker = riga[4]
        region = riga[5]
        charges = riga[6]

        # utilizzo fake.date_between per ottenere delle date del 2024
        start_date = fake.date_between(start_date=datetime.datetime(2024, 1, 1),
                                       end_date=datetime.datetime(2024, 12, 31))
        # estraggo anno, mese e giorno
        year = start_date.year
        month = start_date.month
        day = start_date.day

        try:
            # sostituisco l'anno con 2005 per avere la data di scadenza della polizza
            end_date = start_date.replace(year=2025)
        except ValueError as e:
            # ma devo impostare una data valida nel caso ci fosse un errore
            print(f"Errore nella data: {e}, impostata una data valida")
            # una data valida potrebbe essere il 2025-12-31
            end_date = datetime.date(2025, 12, 31)

        # determino se la polizza è attiva o scaduta
        if end_date < datetime.date.today():
            status = "expired"
        else:
            status = "active"

        # aggiungo i valori nella lista
        policies.append((charges, start_date, end_date, status))

print(policies)

# inserisco i dati nella tabella policies
query_policies = """
INSERT INTO policies (charges, start_date, end_date, status) VALUES (%s, %s, %s, %s)"""

for d in policies:
    esegui_query_parametrizzata(query_policies, d)
