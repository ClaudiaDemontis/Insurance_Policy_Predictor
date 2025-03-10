import joblib
import pandas as pd

# Carica modello e preprocessor
model = joblib.load('modello_regressione_lineare.pkl')
preprocessor = joblib.load('preprocessor.pkl')

nuovo_dato = pd.DataFrame({
    'age': [20],
    'bmi': [30.0],
    'children': [1],
    'sex_male': [0],
    'smoker_yes': [0],
    'region_northeast': [1],
    'region_northwest': [0],
    'region_southeast': [0],
    'region_southwest': [0]
})

# Scala il dato
nuovo_dato_scaled = preprocessor.transform(nuovo_dato)

# Fai la previsione
previsione = model.predict(nuovo_dato_scaled)
print(f"Previsione: {previsione[0]:.2f}")