import pandas as pd
import mysql.connector
import random
from faker import Faker
df = pd.read_csv('insurance_modified.csv')


# Creare un'istanza di Faker
fake = Faker()

# Connessione al database MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='insurance_db'
)
cursor = conn.cursor()

import pandas as pd

# Dati esemplificativi delle regioni negli Stati Uniti (sostituire con dati reali)
regions_data = {
    "name": ["Northeast", "Midwest", "South", "West"],
    "population": [55900000, 68000000, 125000000, 78000000],  # Popolazione per area
    "crime_rate": [4.5, 5.3, 6.8, 3.2],  # Tasso di criminalità per 100,000 abitanti (esempio)
    "unemployment_rate": [5.3, 4.6, 6.1, 4.4],  # Tasso di disoccupazione (%)
    "avg_income": [57000, 50000, 45000, 65000],  # Reddito medio (USD)
    "extreme_weather_events": [3, 6, 7, 5]  # Eventi climatici estremi per anno (esempio)
}

# Creare un DataFrame con questi dati
regions_df = pd.DataFrame(regions_data)

# Visualizzare i dati
print(regions_df)