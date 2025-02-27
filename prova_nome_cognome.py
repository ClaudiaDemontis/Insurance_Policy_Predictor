import csv
from faker import Faker
import mysql.connector
from mysql.connector import Error

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

def esegui_query_place(query, values):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="insurance_db"
        )
        if connection.is_connected():
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                connection.commit()
                print(f"Query eseguita con successo: {query}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

with open("Insurance_cleaned.csv", encoding="utf-8") as f:
    dati = csv.reader(f)
    next(dati)

    fake = Faker()

    fake.email()

    # creo una lista vuota data
    data = []

    for riga in dati:
        nome_cognome = fake.name()  # restiruisce nome e cognome
        lista_nome_cognome = nome_cognome.split()

        # quindi splittiamo il nome e il cognome
        name = lista_nome_cognome[0]
        surname = lista_nome_cognome[1]

        # con questi dati creo le mail
        mail = f"{name.lower()}.{surname.lower()}@example.com"

        # ora creo l'anno di nascita
        age = float(riga[0])
        birth_year = 2025 - age

        # aggiungo nome, cognome, mail nella lista data
        data.append((name, surname, birth_year, mail))

print(data)


query_persona_info = """
INSERT INTO personal_info (name, surname, birth_year, mail) VALUES (%s, %s, %s, %s)"""

for d in data:
    esegui_query_place(query_persona_info, d)