import csv
from faker import Faker
with open("Insurance_cleaned.csv", encoding="utf-8") as f:
    dati = csv.reader(f)
    next(dati)

    fake = Faker()
    nome_cognome = fake.name() # restiruisce nome e cognome
    fake.email()
    lista_nome_cognome = nome_cognome.split()

    nome = lista_nome_cognome[0]
    cognome = lista_nome_cognome[1]
    print(f"{nome}, {cognome}")
