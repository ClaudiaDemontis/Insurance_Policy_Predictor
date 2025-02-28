import csv
from funzioni_utili import esegui_query_parametrizzata, recupera_dati_completi
from funzioni_utili import recupera_dati

# Dizionario per tenere traccia di quante volte è stato usato ogni charges
charges_counter = {}

# Leggo il CSV
with open("Insurance_cleaned.csv", encoding="utf-8") as f:
    dati = csv.reader(f)
    next(dati)  # Salto l'intestazione

    clients = []
    id_personal = 1  # Contatore per ID personale
    indice = 1

    for riga in dati:
        age = riga[0]
        sex = riga[1]
        bmi = riga[2]
        children = riga[3]
        smoker = riga[4]
        region = riga[5]
        charges = riga[6]

        id_region = recupera_dati(f"""SELECT Regions.regional_id
                                    FROM Regions
                                    WHERE Regions.name = "{region}" """)

        id_policy_list = recupera_dati_completi(f"""SELECT Policies.policy_id 
                                    FROM Policies 
                                    WHERE Policies.charges = "{charges}" """)

        # Se ci sono più polizze con lo stesso charges, scegliamo la successiva disponibile
        if charges not in charges_counter:
            charges_counter[charges] = 1  # Inizializziamo il contatore
        else:
            charges_counter[charges] += 1  # Incrementiamo il contatore

        # print(charges )
        # print(id_policy_list)

        #print(charges_counter)
        if charges_counter[charges] != 1:
            id_policy = id_policy_list[indice]
            indice += 1
        else:
            id_policy = id_policy_list[0]   # se la lista restituita ha un solo elemento, prendo quello

        # Aggiungiamo il cliente alla lista
        clients.append((age, sex, float(bmi), children, smoker, id_region[0], id_policy[0], id_personal))

        id_personal += 1  # Incrementiamo il contatore ID personale


# Inserisco i dati nella tabella
query_clients = """
INSERT INTO Clients (age, sex, bmi, children, smoker, id_region, id_policy, id_personal)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

for d in clients:
    esegui_query_parametrizzata(query_clients, d)