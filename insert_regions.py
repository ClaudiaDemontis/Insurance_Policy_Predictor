# --- INSERT REGIONS ---

# Imports
from funzioni_utili import esegui_query

# Inserimento dei dati nella tabella
query_regions = """
INSERT INTO Regions (name, population, crime_rate, unemployment_rate, avg_income, extreme_weather_events) VALUES
('Northeast', 57000000, 0.23, 3.72, 96859, 21.67),
('Southeast', 101000000, 0.35, 3.70, 78320, 27.50),
('Northwest', 15500000, 0.27, 3.80, 82624, 16.67),
('Southwest', 53700000, 0.30, 4.45, 77453, 25.50);
"""

esegui_query(query_regions)



