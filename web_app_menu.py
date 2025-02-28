import mysql.connector
from mysql.connector import Error
from funzioni_utili import esegui_query_parametrizzata
from datetime import datetime,date

# Creo il menu del database
while True:
    print("--- INSURANCE DB ---")
    print("1) Inserisci polizza")
    print("2) Modifica polizza")
    print("3) Elimina polizza")
    print("0) Esci")

    scelta = int(input("Scelta: "))

    # se viene scelta l'opzione "Inserisci polizza"
    if scelta == 1:
        # inserire i dati personali del cliente
        print("\nInserire i dati personali del cliente.")
        name = input("Nome: ")
        surname = input("Cognome: ")
        birth_year = int(input("Anno di nascita: "))
        mail = input("Mail: ")

        # inserisco i dati in un dizionario vuoto
        dati_personali_cliente = []
        dati_personali_cliente.append((name, surname, birth_year, mail))
        print(dati_personali_cliente)

        # inserire i dati medici del cliente
        print("\nInserire i dati medici del clienti.")
        age = 2025 - birth_year
        sex = input("Sex (Male/Female): ")
        bmi = input("Body mass index: ")
        children = input("Children (n): ")
        smoker = input("Smoker (Yes/No): ")
        # region = input("Region: ")
        # policy = input("Policy: ")
        # personal_info = input("Personal info: ")

        # inserisco i dati in un dizionario vuoto
        dati_medici_cliente = []
        dati_medici_cliente.append((age, sex, bmi, children, smoker))
        print(dati_medici_cliente)

        # inserire i dati della polizza assicurativa del cliente
        print("Inserire i dati della polizza assicurativa del cliente.")
        charges = float(input("Charges: "))

        # inseriamo una data di inizio che non sia superirore al giorno corrente
        # e impostiamo la data di fine allo stesso giorno dell'anno successivo
        while True:
            try:
                start_date_input = input("Data di inizio (YYYY-MM-DD): ")
                year, month, day = map(int, start_date_input.split('-'))
                start_date = date(year, month, day)

                # Verifico che la data di inizio non sia nel futuro
                if start_date > date.today():
                    print("La data di inizio NON PUO' essere nel futuro, inserire una data valida.")
                else:
                    break
            except ValueError:
                print("Formato data non valido. Usa il formato YYYY-MM-DD.")

        # calcolo della data di fine
        try:
            end_date = start_date.replace(year=start_date.year + 1)
        except ValueError:
            # se la data di fine non è valida (es. 29 febbraio in un anno non bisestile), viene impostata una data valida
            print("Errore nella data di fine, impostata una data valida.")
            end_date = date(start_date.year + 1, 3, 1)  # viene impostata la data di fine al 1 marzo dell'anno successivo

        # imposto se la polizza è attiva o scaduta
        if end_date > date.today():
            status = "Active"
        else:
            status = "Expired"

        # inserisco i dati in un dizionario vuoto
        dati_polizza = []
        dati_polizza.append((charges, start_date, end_date, status))
        print(dati_polizza)

        # query per inserire i dati nel database
        query_dati_personali = """INSERT INTO personal_info (name, surname, birth_year, mail) 
                                    VALUES (%s, %s, %s, %s)"""
        # for d in dati_personali:
        #     esegui_query_parametrizzata(query_dati_personali, d)

        query_dati_medici = """INSERT INTO Clients (age, sex, bmi, children, smoker, id_region, id_policy, id_personal)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        # for d in dati_medici:
        #     esegui_query_parametrizzata(query_dati_medici, d)

        query_dati_polizza = """INSERT INTO policies (charges, start_date, end_date, status) 
                                    VALUES (%s, %s, %s, %s)"""
        # for d in dati_polizza:
        #     esegui_query_parametrizzata(query_dati_polizza, d)


    if scelta == 2:
        print("1. Aggiorna dati personali Cliente")
        print("2. Aggiorna dati medici Cliente")
        print("2. Aggiorna dati polizza Cliente")

        scelta = input("Scelta: ")

        if scelta

    if scelta == 3:
        print("1) Dati Personali")
        print("2) Clienti")
        print("3) Polizze")
        print("0) Esci")

        scelta = input("Scelta: ")

    if scelta == 0:
        break