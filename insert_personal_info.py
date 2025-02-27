# --- INSERT PERSONAL INFO ---

# imports
import csv
from faker import Faker
import mysql.connector
from mysql.connector import Error
from funzioni_utili import esegui_query_parametrizzata

# Inserimento dei dati nella tabella
def esegui_query(query):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="olympics_db"
        )
        if connection.is_connected():
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                print(f"Query eseguita con successo: {query}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# leggo il csv
with open("Insurance_cleaned.csv", encoding="utf-8") as f:
    dati = csv.reader(f)
    next(dati)

    fake = Faker()

    fake.email()

    # creo una lista vuota data
    data = []

    # creo i nomi e i cognomi con la libreria faker
    for riga in dati:

        if riga[1] == "male":
            name = fake.first_name_male()
            surname = fake.last_name()
        else:
            name = fake.first_name_female()
            surname = fake.last_name()

        # con questi dati creo le mail
        mail = f"{name.lower()}.{surname.lower()}@example.com"

        # creo anche l'anno di nascita
        age = float(riga[0])
        birth_year = 2025 - age

        # aggiungo nome, cognome, mail nella lista data
        data.append((name, surname, birth_year, mail))

print(data)

# inserisco i dati nella tabella
query_persona_info = """
INSERT INTO personal_info (name, surname, birth_year, mail) VALUES (%s, %s, %s, %s)"""

for d in data:
    esegui_query_parametrizzata(query_persona_info, d)