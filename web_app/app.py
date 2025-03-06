from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
from funzioni_utili import recupera_dati
from funzioni_utili import recupera_dati_completi
from funzioni_utili import esegui_query_parametrizzata
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("esempio_sito.html")

@app.route("/dati_assicurativi")
def dati_assicurativi():
    return render_template("dati_assicurativi.html")


@app.route("/gestione_clienti")
def gestione_clienti():
    return render_template("gestione_clienti.html")


@app.route("/gestione_clienti/search", methods=["POST"])
def search():
    # nome = request.form.get("clienteNome")  # funziona
    nome = request.form["clienteNome"]
    prezzo = request.form["clienteCharges"]
    print(nome)
    print(prezzo)
    q = f"""SELECT Clients.client_id, Personal_Info.name, Personal_Info.surname,
    Personal_Info.mail, Clients.id_policy, Policies.charges
    FROM Clients INNER JOIN Personal_Info
    ON Clients.id_personal = Personal_Info.personal_id
    INNER JOIN Policies ON Policies.policy_id = Clients.id_policy
    WHERE 1 
    """
    if nome != "":
        q += f""" AND (Personal_Info.name LIKE "%{nome}%" OR Personal_Info.surname LIKE "%{nome}%") """
    if prezzo != "":
        q += f""" AND Policies.charges > {prezzo} """
    print(q)
    risultati = recupera_dati_completi(q)
    print(risultati)

    return render_template("gestione_clienti.html", risultati=risultati)

@app.route("/gestione_clienti/inserisci_cliente", methods=["GET", "POST"])
def inserisci_cliente():
    if request.method == "POST":
        nome = request.form["nome"]
        cognome = request.form["cognome"]
        anno_nascita = request.form["anno_nascita"]
        eta = request.form["eta"]
        email = request.form["email"]
        sesso = request.form["sesso"]
        bmi = request.form["bmi"]
        fumatore = request.form["fumatore"]
        regione_residenza = request.form["regione_residenza"]
        id_polizza = request.form["id_polizza"]

        # Creazione del cliente (puoi sostituire con la logica di salvataggio nel DB)
        nuovo_cliente = {
            'nome': nome,
            'cognome': cognome,
            'anno_nascita': anno_nascita,
            'eta': eta,
            'email': email,
            'sesso': sesso,
            'bmi': bmi,
            'fumatore': fumatore,
            'regione_residenza': regione_residenza,
            'id_polizza': id_polizza }
        print(nuovo_cliente)
        query_personal_info = """ INSERT INTO Personal_Info(name, surname, birth_year, mail) VALUES
        (%s, %s, %s, %s) """
        tupla_personal_info = (nome, cognome, anno_nascita, email)
        esegui_query_parametrizzata(query_personal_info, tupla_personal_info)
        print(regione_residenza)
        id_region = recupera_dati(f"""SELECT Regions.regional_id FROM Regions WHERE Regions.name = '{regione_residenza}'""")
        print(id_region)
        tupla_clients = (eta, sesso, bmi, fumatore, id_region[0])
        query_clients = ("""INSERT INTO Clients (age, sex, bmi, smoker, id_region) VALUES
        (%s, %s, %s, %s, %s) """ )
        esegui_query_parametrizzata(query_clients, tupla_clients)
        messaggio = f"""L'utente {nome} {cognome} è stato inserito correttamente."""

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


    return render_template("inserisci_cliente.html")


@app.route('/gestione_clienti/elimina_cliente/<int:id>')
def elimina_cliente(id):
    print(f"Sto eliminando il cliente con ID: {id}")
    query = "DELETE FROM Clients WHERE Clients.id_personal = %s"
    esegui_query_parametrizzata(query, (id,))

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

# @app.route("/gestione_clienti/elimina_cliente", methods=["POST"])
# def elimina_cliente():
#     nome = request.form.get("clienteNome","")  # funziona
#     #nome = request.form["clienteNome"]
#     pass

@app.route("/gestione_clienti/modifica_cliente", methods=["POST"])
def modifica_cliente():
    nome = request.form.get("clienteNome","")  # funziona
    #nome = request.form["clienteNome"]
    pass

@app.route("/gestione_polizze")
def gestione_polizze():
    return render_template("gestione_polizze.html")


if __name__ == "__main__":
    app.run(debug=True)