# Import section
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
import joblib

# Caricamento del dataset
df = pd.read_csv('Insurance_cleaned.csv')

# Visualizzazione iniziale
print(df.head())
print(df.columns)
print(df.describe())

# Conversione delle variabili categoriche
df = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=True)

# Selezione delle variabili indipendenti e dipendenti
X = df.drop(columns=['charges'])
y = df['charges']

# Split del dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

# Selezione delle colonne numeriche
colonne_numeriche = ['age', 'bmi', 'children']

# Preprocessing: scaler solo sulle colonne numeriche
preprocessor = ColumnTransformer(
    [('scaler', StandardScaler(), colonne_numeriche)],
    remainder='passthrough'
)

# Scaling dei dati
X_train_scaled = preprocessor.fit_transform(X_train)
X_test_scaled = preprocessor.transform(X_test)

# Addestramento del modello di regressione lineare
model = LinearRegression(fit_intercept=True)
model.fit(X_train_scaled, y_train)

# Valutazione del modello
test_pred = model.predict(X_test_scaled)
print("\nMetriche del modello di regressione lineare:")
print('MSE:', mean_squared_error(y_test, test_pred))
print('MAE:', mean_absolute_error(y_test, test_pred))
print('RMSE:', math.sqrt(mean_squared_error(y_test, test_pred)))
print("Media della colonna charges:", df["charges"].mean())

# === PREVISIONE SU DATO INSERITO MANUALMENTE ===
# Inserisci qui i tuoi dati manuali
nuovo_dato = pd.DataFrame({
    'age': [35],
    'bmi': [28.5],
    'children': [2],
    'sex_male': [1],            # 1 se male, 0 se female
    'smoker_yes': [0],          # 1 se yes, 0 se no
    'region_northeast': [1],    # Imposta a 1 la regione scelta, le altre a 0
    'region_northwest': [0],
    'region_southeast': [0],
    'region_southwest': [0]
})

# Scaling del dato manuale
nuovo_dato_scaled = preprocessor.transform(nuovo_dato)

# Predizione
previsione = model.predict(nuovo_dato_scaled)
print(f"\nLa previsione del costo assicurativo per il nuovo dato è: {previsione[0]:.2f}")

# joblib.dump(model, 'modello_regressione_lineare.pkl')
#
# # Salvataggio del preprocessor (scaler + colonne)
# joblib.dump(preprocessor, 'preprocessor.pkl')

