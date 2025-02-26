# --- TABLES CREATION ---
import mysql.connector
from mysql.connector import Error

def esegui_query(query):

    try:
        # Create connection
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
        if connection.is_connected():
            connection.close()


# Table Personal_Info
esegui_query("""CREATE TABLE IF NOT EXISTS Personal_Info (
    personal_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    surname VARCHAR(255),
    birth_year INT,
    mail VARCHAR(255) UNIQUE
);""")

# Table Regions
esegui_query("""CREATE TABLE IF NOT EXISTS Regions (
    regional_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    population INT,
    crime_rate FLOAT,
    unemployment_rate FLOAT,
    avg_income FLOAT,
    extreme_weather_events INT
);""")

# Table Policies
esegui_query("""CREATE TABLE IF NOT EXISTS Policies (
    policy_id INT PRIMARY KEY AUTO_INCREMENT,
    charges FLOAT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50) CHECK (status IN ('active', 'expired'))
);""")

# Table Clients
esegui_query("""CREATE TABLE IF NOT EXISTS Clients (
    client_id INT PRIMARY KEY AUTO_INCREMENT,
    age INT,
    sex VARCHAR(10) CHECK (sex IN ('female', 'male')),
    bmi FLOAT,
    children INT,
    smoker VARCHAR(10) CHECK (smoker IN ('yes', 'no')),
    id_region INT,
    id_policy INT,
    id_personal INT,
    FOREIGN KEY (id_region) REFERENCES Regions(regional_id),
    FOREIGN KEY (id_policy) REFERENCES Policies(policy_id),
    FOREIGN KEY (id_personal) REFERENCES Personal_Info(personal_id)
);""")