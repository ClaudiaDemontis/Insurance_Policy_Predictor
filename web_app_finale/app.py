import datetime

from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
# from socks import method

from funzioni_utili import recupera_dati
from funzioni_utili import recupera_dati_completi
from funzioni_utili import esegui_query_parametrizzata
from funzioni_utili import esegui_query
from decimal import Decimal
import pandas as pd
from datetime import date, datetime, timedelta
import joblib


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("esempio_sito.html")

@app.route("/dati_assicurativi")
def dati_assicurativi():
    # Carica il CSV in un DataFrame (modifica il path al tuo file CSV)
    df = pd.read_csv('insurance_cleaned.csv')
    # Converti il DataFrame in una lista di dizionari per l'HTML
    dati = df.to_dict(orient="records")

    # Numero di elementi per pagina
    per_page = 25
    page = request.args.get("page", 1, type=int)
    total_pages = (len(dati) // per_page) + (1 if len(dati) % per_page > 0 else 0)

    # Seleziona i dati per la pagina attuale
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    dati_paginati = dati[start_idx:end_idx]

    return render_template("dati_assicurativi.html", dati=dati_paginati, page=page, total_pages=total_pages)
    # Converte il DataFrame in HTML per visualizzarlo


@app.route("/gestione_clienti")
def gestione_clienti():
    return render_template("gestione_clienti.html")


@app.route("/gestione_clienti/search", methods=["GET", "POST"])
def search():
    # nome = request.form.get("clienteNome")  # funziona
    nome = request.form["clienteNome"]
    cognome = request.form["clienteCognome"]
    prezzo = request.form["clienteCharges"]
    genere = request.form["genere"]
    stato = request.form["stato"]

    print(nome)
    print(prezzo)
    print(genere)
    #print(genere_donna)
    q = f"""SELECT Clients.client_id, Personal_Info.name, Personal_Info.surname,
    Personal_Info.mail, Clients.id_policy, Policies.status, Policies.charges
    FROM Clients INNER JOIN Personal_Info
    ON Clients.id_personal = Personal_Info.personal_id
    LEFT JOIN Policies ON Policies.policy_id = Clients.id_policy
    WHERE 1 
    """
    if nome != "":  # se inserisco il nome
        q += f""" AND (Personal_Info.name LIKE "%{nome}%") """
    if cognome != "":   # se inserisco il cognome
        q += f""" AND (Personal_Info.surname LIKE "%{cognome}%") """
    if prezzo != "":
        q += f""" AND Policies.charges > {prezzo} """
    if genere == "Uomo":
        q += f""" AND Clients.sex = 'male' """
    if genere == "Donna":
        q += f""" AND Clients.sex = 'female' """
    if stato == "Attiva":
        q += f""" AND Policies.status = 'active' """
    if stato == "Scaduta":
        q += f""" AND Policies.status = 'expired' """

    print(q)
    risultati = recupera_dati_completi(q)
    # se un elemento di risultati è None, lo sostituisco con '' per visualizzarlo nella tabella html
    print(f" PRIMA: {risultati}")
    # creo una nuova tupla in cui sostiutisco None con ''
    risultati = [tuple(0 if valore is None else valore for valore in riga) for riga in risultati]
    # se è active stampo attivo, altrimenti inattivo
    risultati = [tuple("attiva" if valore == "active" else valore for valore in riga) for riga in risultati]
    risultati = [tuple("scaduta" if valore == "expired" else valore for valore in riga) for riga in risultati]

    #print(risultati[0][6])

    print(f" DOPO: {risultati}")

    # Controlla se l'utente ha richiesto un ordinamento

    # sort_by = request.args.get('sort')  # Es. "nome", "id", "premio"
    #
    # if risultati:
    #     if sort_by == "nome":
    #         risultati = sorted(risultati, key=lambda x: (x[1], x[2]))  # Nome e Cognome
    #     elif sort_by == "id":
    #         risultati = sorted(risultati, key=lambda x: x[0])  # ID Cliente
    #     elif sort_by == "premio":
    #         try:
    #             risultati = sorted(risultati, key=lambda x: float(x[6]))  # Premio Annuo
    #         except ValueError:
    #             pass  # Evita errori se ci sono valori non validi in charges

    return render_template("gestione_clienti.html", risultati=risultati)


@app.route("/gestione_clienti/inserisci_cliente", methods=["GET", "POST"])
def inserisci_cliente():
    if request.method == "POST":
        nome = request.form["nome"]
        cognome = request.form["cognome"]
        anno_nascita = request.form["anno_nascita"]
        email = request.form["email"]
        numero_figli = request.form["numero_figli"]
        sesso = request.form["sesso"]
        bmi = request.form["bmi"]
        fumatore = request.form["fumatore"]
        regione_residenza = request.form["regione_residenza"]

        if bmi == '':
            bmi = None
        # if id_polizza == '':
        #     id_polizza = None
        if sesso == 'Donna':
            sesso = 'female'
        if sesso == 'Uomo':
            sesso = 'male'

        if fumatore == "Sì":
            fumatore = "yes"
        if fumatore == "No":
            fumatore == "no"


        # Creazione del cliente
        nuovo_cliente = {
            'nome': nome,
            'cognome': cognome,
            'anno_nascita': anno_nascita,
            'email': email,
            'sesso': sesso,
            'bmi': bmi,
            'figli': numero_figli,
            'fumatore': fumatore,
            'regione_residenza': regione_residenza }
        print(nuovo_cliente)

        # Inserisco i dati cliente in Personal_Info
        query_personal_info = """ INSERT INTO Personal_Info(name, surname, birth_year, mail) VALUES
        (%s, %s, %s, %s) """
        tupla_personal_info = (nome, cognome, anno_nascita, email)
        esegui_query_parametrizzata(query_personal_info, tupla_personal_info)

        # Inserimento (opzionale) della polizza
        charges = request.form["premium"]
        data_inizio = request.form["date"]
        print(f"{data_inizio=}")
        print(type(data_inizio))


        # Converte la stringa in oggetto datetime
        data_inizio_dt = datetime.strptime(data_inizio, "%Y-%m-%d")

        # Calcola la data di fine polizza aggiungendo un anno
        data_fine_dt = data_inizio_dt + timedelta(days=365)

        # Converti nuovamente in stringa se necessario
        data_fine = data_fine_dt.strftime("%Y-%m-%d")


        status = "active"

        tupla_policies = (charges, data_inizio, data_fine, status)
        query_policies = """INSERT INTO Policies (charges, start_date, end_date, status)
                VALUES (%s, %s, %s, %s)"""
        print(query_policies)
        esegui_query_parametrizzata(query_policies, tupla_policies)
        # Recupero l'id della polizza appena inserita
        id_polizza = recupera_dati(f""" SELECT Policies.policy_id 
                FROM Policies 
                WHERE Policies.charges = {charges} AND Policies.start_date = "{data_inizio}" """)[0]
        if id_polizza is None:
            id_polizza = 0
        print(id_polizza)

        # Ricavo l'id della regione inserita
        print(regione_residenza)
        id_region = recupera_dati(f"""SELECT Regions.regional_id FROM Regions WHERE Regions.name = '{regione_residenza}'""")
        print(id_region)
        # Ricavo l'id_personal del cliente appena inserito usando la chiave mail che è unique
        id_personal = recupera_dati(f"""SELECT Personal_Info.personal_id 
                                        FROM Personal_Info
                                        WHERE Personal_Info.mail = "{email}" """)
        print(id_personal)
        # Calcolo l'età in base all'anno di nascita
        eta = int(date.today().year - int(anno_nascita))


        # Inserisco i dati del cliente in Clients
        tupla_clients = (eta, sesso, bmi, numero_figli, fumatore, id_region[0], id_polizza, id_personal[0])
        print(tupla_clients)
        query_clients = ("""INSERT INTO Clients (age, sex, bmi, children, smoker, id_region, id_policy, id_personal) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s) """ )
        esegui_query_parametrizzata(query_clients, tupla_clients)



        messaggio = f"""L'utente {nome} {cognome} è stato inserito correttamente."""

        # Restituire una risposta HTML che contiene uno script per il popup
        return f"""
        <html>
            <head>
                <script type="text/javascript">
                    alert("{messaggio}");
                    window.location.href = "/gestione_clienti/inserisci_cliente";
                </script>
            </head>
            <body>
                <!-- Questa parte non sarà visibile perché il popup verrà mostrato subito -->
            </body>
        </html>
    """


    return render_template("inserisci_cliente.html")


@app.route('/gestione_clienti/elimina_cliente/<int:id>', methods=["GET", "POST"])
def elimina_cliente(id):  # l'id in questione è client_id
    print(f"Sto eliminando il cliente con client_id: {id}")

    # Recupero il personal_id corrispondente a quel client_id
    query = f"SELECT Clients.id_personal FROM Clients WHERE Clients.client_id = {id}"
    personal_id = recupera_dati(query)[0]
    print(query)
    print(f"{personal_id}=")

    # Recupero il personal_id corrispondente a quel client_id
    query = f"SELECT Policies.policy_id FROM Clients INNER JOIN Policies ON Clients.id_policy = Policies.policy_id WHERE Clients.client_id = {id}"
    policy_id = recupera_dati(query)[0]
    print(query)
    print(f"{policy_id}=")

    # Elimina il cliente dalla tabella Clients
    query_clients = "DELETE FROM Clients WHERE Clients.client_id = %s"
    esegui_query_parametrizzata(query_clients, (id,))
    print(f"Eliminato il cliente dalla tabella Clients per client_id {id}")

    # Elimina il cliente dalla tabella Policies (prima di Personal_info)
    query_policy = """DELETE FROM Policies
                      WHERE policy_id = %s"""

    esegui_query_parametrizzata(query_policy, (policy_id,))

    # Elimina il cliente dalla tabella Personal_info
    query_personal = """DELETE FROM Personal_info
                        WHERE personal_id = %s"""

    esegui_query_parametrizzata(query_personal, (personal_id,))

    print(f"Eliminato il cliente dalla tabella Clients per client_id {id}")

    # Ho aggiunto questo direttamente nel database
    # ALTER TABLE Personal_info
    # ADD CONSTRAINT fk_personal_info_client
    # FOREIGN KEY (personal_id)
    # REFERENCES Clients(id_personal)
    # ON DELETE CASCADE;

    # ALTER TABLE Policies
    # ADD CONSTRAINT fk_policies_client
    # FOREIGN KEY (policy_id)
    # REFERENCES Clients(id_policy)
    # ON DELETE CASCADE;

    # Creazione del messaggio da visualizzare nel popup
    messaggio = f"Cliente con ID {id} eliminato"

    # Restituire una risposta HTML che contiene uno script per il popup
    return f"""
    <html>
        <head>
            <script type="text/javascript">
                alert("{messaggio}");
                window.location.href = "/gestione_clienti";  // Redirigi a una pagina di gestione clienti
            </script>
        </head>
        <body>
            <!-- Questa parte non sarà visibile perché il popup verrà mostrato subito -->
        </body>
    </html>
    """


@app.route("/about")
def about():

    return render_template("about.html")


@app.route("/gestione_clienti/modifica_cliente/<int:id>", methods=["GET", "POST"])
def modifica_cliente(id):
    if request.method == "POST":
        nome = request.form["nome"]
        cognome = request.form["cognome"]
        email = request.form["email"]
        anno_nascita = request.form["anno_nascita"]
        sesso = request.form["sesso"]
        bmi = request.form["bmi"]
        numero_figli = request.form["numero_figli"]
        fumatore = request.form["fumatore"]
        regione_residenza = request.form["regione_residenza"]



        # Calcolo l'età in base all'anno di nascita
        eta = int(date.today().year - int(anno_nascita))
        print(eta)

        id_region = recupera_dati(f"""SELECT regional_id FROM Regions WHERE name = '{regione_residenza}'""")
        query_clients = """UPDATE Clients SET age = %s, sex = %s, bmi = %s, children = %s, smoker = %s, id_region = %s WHERE client_id = %s"""
        tupla_clients = (eta, sesso, bmi, numero_figli, fumatore, id_region[0], id)
        esegui_query_parametrizzata(query_clients, tupla_clients)

        # Aggiorno i dati nella tabella Personal_info
        query_personal_info = """UPDATE Personal_info
                                 INNER JOIN Clients ON Personal_info.personal_id = Clients.id_personal
                                 SET Personal_info.name = %s, Personal_info.surname = %s, Personal_info.mail = %s, Personal_info.birth_year = %s 
                                 WHERE Clients.client_id = %s"""
        tupla_personal_info = (nome, cognome, email, anno_nascita, id)
        esegui_query_parametrizzata(query_personal_info, tupla_personal_info)

        # Inserimento dei dati della polizza
        charges = request.form["premium"]
        data_inizio = request.form["date"]
        print(f"{data_inizio=}")
        print(type(data_inizio))

        # Converte la stringa in oggetto datetime
        data_inizio_dt = datetime.strptime(data_inizio, "%Y-%m-%d")

        # Calcola la data di fine polizza aggiungendo un anno
        data_fine_dt = data_inizio_dt + timedelta(days=365)

        # Converte nuovamente in stringa se necessario
        data_fine = data_fine_dt.strftime("%Y-%m-%d")
        start_date = data_inizio_dt.strftime("%Y-%m-%d")  # Rendi `data_inizio_dt` una stringa nel formato corretto

        # Stato della polizza (attivo)
        status = "active"

        # Aggiorno i dati nella tabella policies
        query_policies = """UPDATE Policies
                            INNER JOIN Clients ON Policies.policy_id = Clients.id_policy
                            SET Policies.charges = %s, Policies.start_date = %s, Policies.end_date = %s, Policies.status = %s
                            WHERE Clients.client_id = %s"""
        tupla_policies = (charges, start_date, data_fine, status, id)

        # Esegui la query parametrizzata
        esegui_query_parametrizzata(query_policies, tupla_policies)

        messaggio = f"""Dati modificati correttamente."""

        # Redirigi l'utente a una pagina di conferma o ad un'altra pagina
        # Restituire una risposta HTML che contiene uno script per il popup
        return f"""
                <html>
                    <head>
                        <script type="text/javascript">
                            alert("{messaggio}");
                            window.location.href = "/gestione_clienti";  // Redirigi a una pagina di gestione clienti
                        </script>
                    </head>
                    <body>
                        <!-- Questa parte non sarà visibile perché il popup verrà mostrato subito -->
                    </body>
                </html>
            """
    else:
        q = f"""SELECT Clients.client_id, Personal_Info.name, Personal_Info.surname, Personal_Info.birth_year, Personal_Info.mail, Clients.children, Clients.sex, Clients.bmi, Clients.smoker, Regions.name, Policies.charges, Policies.start_date
                                           FROM Clients
                                           INNER JOIN Personal_Info ON Clients.id_personal = Personal_Info.personal_id
                                           INNER JOIN Regions ON Clients.id_region = Regions.regional_id
                                           INNER JOIN Policies ON Clients.id_policy = Policies.policy_id
                                           WHERE Clients.client_id = {id}"""
        print(q)
        cliente = recupera_dati_completi(f"""SELECT Clients.client_id, Personal_Info.name, Personal_Info.surname, Personal_Info.birth_year, Personal_Info.mail, Clients.children, Clients.sex, Clients.bmi, Clients.smoker, Regions.name, Policies.charges, Policies.start_date
                                           FROM Clients
                                           INNER JOIN Personal_Info ON Clients.id_personal = Personal_Info.personal_id
                                           INNER JOIN Regions ON Clients.id_region = Regions.regional_id
                                           INNER JOIN Policies ON Clients.id_policy = Policies.policy_id
                                           WHERE Clients.client_id = {id}""")
        print(cliente)
        return render_template("modifica_cliente.html", cliente=cliente[0])



@app.route("/premio", methods=["GET", "POST"])
def premio():
    previsione = None  # Valore iniziale
    age = bmi = children = sex = smoker = region = None  # Aggiungi i dati da visualizzare

    if request.method == 'POST':
        # Recupero dati dal form
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        children = request.form['children']
        sex = request.form['sex']
        smoker = request.form['smoker']
        region = request.form['region']

        # Converte i valori testuali in numerici
        children = 1 if children == "yes" else 0
        sex = 1 if sex == "male" else 0
        smoker = 1 if smoker == "yes" else 0
        region_mapping = {"northeast": 0, "northwest": 1, "southeast": 2, "southwest": 3}
        region = region_mapping.get(region, -1)

        # Carica modello e preprocessor
        model = joblib.load('modello_regressione_lineare.pkl')
        preprocessor = joblib.load('preprocessor.pkl')

        nuovo_dato = pd.DataFrame({
            'age': [age],
            'bmi': [bmi],
            'children': [children],
            'sex_male': [sex],
            'smoker_yes': [smoker],
            'region_northeast': [1 if region == 0 else 0],
            'region_northwest': [1 if region == 1 else 0],
            'region_southeast': [1 if region == 2 else 0],
            'region_southwest': [1 if region == 3 else 0]
        })

        # Scala il dato
        nuovo_dato_scaled = preprocessor.transform(nuovo_dato)

        # Fai la previsione
        previsione = model.predict(nuovo_dato_scaled)
        print(f"Previsione: {previsione[0]:.2f}")

        return render_template('premio.html', prediction=previsione[0], age=age, bmi=bmi, children=children, sex=sex, smoker=smoker, region=region)

    return render_template('premio.html', prediction=previsione, age=age, bmi=bmi, children=children, sex=sex, smoker=smoker, region=region)



if __name__ == "__main__":
    app.run(debug=True)