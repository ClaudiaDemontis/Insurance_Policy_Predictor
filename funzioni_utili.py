# --- FUNCTIONS ---
import mysql.connector
from mysql.connector import Error
#uso questa funzione per le query di inserimento dati, modifica dati, ed eliminazione dati
def esegui_query(query):
    connection = None  # Inizializzo la variabile connection
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="insurance_db"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            print(f"Query eseguita con successo: {query}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection and connection.is_connected():  # Controllo se la connessione è stata creata
            connection.close()


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


def esegui_query_parametrizzata_many(query, parametri):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="insurance_db"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.executemany(query, parametri)
            connection.commit()
            cursor.close()
            print(f"Query eseguita con successo: {query}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

def recupera_dati(query):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="insurance_db"
        )
        if connection.is_connected():
            cursor = connection.cursor()  # Restituisce risultati come dizionari

            # Eseguiamo la query
            cursor.execute(query)

            # Recupero dei dati
            result = [elem[0] for elem in cursor.fetchmany()]

            cursor.close()
            return result
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()
def recupera_dati_completi(query):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="insurance_db"
        )
        if connection.is_connected():
            cursor = connection.cursor()  # Restituisce risultati come dizionari

            # Eseguiamo la query
            cursor.execute(query)

            # Recupero dei dati
            result = [elem for elem in cursor.fetchall()]

            cursor.close()
            return result
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()