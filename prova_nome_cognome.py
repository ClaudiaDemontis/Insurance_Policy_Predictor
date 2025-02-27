import mysql
import csv
from faker import Faker

def esegui_query_parametrizzata(query, parametri):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="insurance_db"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query, parametri)
            connection.commit()
            cursor.close()
            print(f"Dati inseriti correttamente: {parametri}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
    finally:
        if connection.is_connected():
            connection.close()

def esegui_query_parametrizzata_connection(query, parametri, connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query, parametri)
            connection.commit()
            cursor.close()
            print(f"Dati inseriti correttamente: {parametri}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")


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

        # aggiungo nome, cognome, mail nella lista data
        data.append((name, surname, mail))

print(data)







# query_persona_info = """
# INSERT INTO personal_info (name, surname, birth_year, mail) VALUES (%, %, %, %)"""
