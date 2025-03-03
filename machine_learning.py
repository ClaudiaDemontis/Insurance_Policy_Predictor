# Caricamento e esplorazione del dataset
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carica il dataset
df = pd.read_csv('Insurance_cleaned.csv')

# Esplora i primi record del dataset
print(df.head())

# Statistiche descrittive
print(df.describe())

# Visualizzazione dei dati
# Grafico della distribuzione del costo
sns.histplot(df['charges'], kde=True)
plt.title('Distribuzione del costo delle polizze')
plt.show()

# Costruzione del modello di regressione lineare
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Seleziona le variabili indipendenti e dipendenti
X = df.drop(columns=['charges'])
y = df['charges']

# Suddivisione in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modello di regressione lineare
model = LinearRegression()
model.fit(X_train, y_train)

# Predizioni
y_pred = model.predict(X_test)

# Valutazione del modello
print('MSE:', mean_squared_error(y_test, y_pred))
print('R^2:', r2_score(y_test, y_pred))


# 1. Analisi Età-Costo
import matplotlib.pyplot as plt
import seaborn as sns

# Grafico di dispersione tra età e costo
plt.figure(figsize=(10, 6))
sns.scatterplot(x='age', y='charges', data=df)
plt.title('Relazione tra Età e Costo della Polizza')
plt.xlabel('Età')
plt.ylabel('Costo della Polizza')
plt.show()

# Calcolare la correlazione tra età e costo
correlation_age_cost = df['age'].corr(df['charges'])
print(f'Correlazione tra Età e Costo: {correlation_age_cost}')
