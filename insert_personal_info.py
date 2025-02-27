# ------- INSERT PERSONAL INFO -------
# Imports
import csv
from faker import Faker
from funzioni_utili import esegui_query_parametrizzata

# Inserimento dei dati nella tabella
# Leggo il csv
with open("Insurance_cleaned.csv", encoding="utf-8") as f:
    dati = csv.reader(f)
    # Salto la riga dell'intestazione
    next(dati)

    fake = Faker()

    # Creo una lista vuota a cui appenderò i dati da inserire
    data = []

    # Creo i nomi e i cognomi con la libreria faker
    for riga in dati:

        if riga[1] == "male":
            name = fake.first_name_male()
            surname = fake.last_name()
        else:
            name = fake.first_name_female()
            surname = fake.last_name()

        # Con questi dati creo le mail
        mail = f"{name.lower()}.{surname.lower()}@example.com"
        # Mail è un campo 'unique', quindi se abbiamo degli utenti con lo stesso nome dovranno avere delle mail diverse
        # Errore durante l'esecuzione della query: 1062 (23000): Duplicate entry 'melissa.wheeler@example.com' for key 'mail'
        for tupla in data:
            if mail in tupla:
                mail = f"{name.lower()}1.{surname.lower()}@example.com"

        # Creo anche l'anno di nascita
        age = float(riga[0])
        birth_year = 2025 - age

        # Aggiungo nome, cognome, mail nella lista data
        data.append((name, surname, birth_year, mail))

#print(data)

# Inserisco i dati nella tabella
query_persona_info = """
INSERT INTO personal_info (name, surname, birth_year, mail) VALUES (%s, %s, %s, %s)"""

for d in data:
    esegui_query_parametrizzata(query_persona_info, d)
