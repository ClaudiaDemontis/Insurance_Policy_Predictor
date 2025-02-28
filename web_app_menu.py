import mysql.connector
from mysql.connector import Error
from funzioni_utili import esegui_query

while True:
    print("--- INSURANCE DB ---")
    print("1) Inserisci dati")
    print("2) Modifica dati")
    print("3) Elimina dati")
    print("0) Esci")

    scelta = int(input("Scelta: "))

    if scelta == 1:
        print("1) Dati Personali")
        print("2) Clienti")
        print("3) Polizze")
        print("0) Esci")

        scelta2 = input("Scelta: ")

    if scelta == 2:
        print("1) Dati Personali")
        print("2) Clienti")
        print("3) Polizze")
        print("0) Esci")

        scelta3 = input("Scelta: ")

    if scelta == 3:
        print("1) Dati Personali")
        print("2) Clienti")
        print("3) Polizze")
        print("0) Esci")

        scelta4 = input("Scelta: ")

    if scelta == 0:
        break