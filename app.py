from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

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

@app.route("/gestione_polizze")
def gestione_polizze():
    return render_template("gestione_polizze.html")
# def index():
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",  # Inserisci il tuo nome utente
#         password="",  # Inserisci la tua password
#         database="vgsales"  # Inserisci il nome del tuo database
#     )
#     cursor = conn.cursor(dictionary= True)
#     q = """SELECT gioco.nome_gioco, gioco.anno, piattaforma.nome_piattaforma
#         FROM gioco
#         INNER JOIN piattaforma ON gioco.piattaforma_id = piattaforma.id_piattaforma"""
#     cursor.execute(q)
#     risultato = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return render_template("index.html", lista_vg = risultato)
#
#
# #rotta parametrizzata
# # @app.route("/sport/<selected_sport>")
# # def sport_players(selected_sport):
# #     lista_giocatori = []
# #     for elem in players:
# #         if elem["sport"] == selected_sport.lower():
# #             lista_giocatori.append(elem)
# #     #return lista_giocatori
# #     return render_template("index.html", players = lista_giocatori)
#
#

if __name__ == "__main__":
    app.run(debug=True)