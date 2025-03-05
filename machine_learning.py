# Caricamento e esplorazione del dataset
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Carica il dataset
df = pd.read_csv('Insurance_cleaned.csv')

#converto le variabili non numeriche
df = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=True)

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
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

# Seleziona le variabili indipendenti e dipendenti
X = df.drop(columns=['charges'])
y = df['charges']

#grafico iniziale


# Suddivisione in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
# we are going to scale ONLY the features (i.e. the X) and NOT the y!
X_train_scaled = scaler.fit_transform(X_train) # fitting to X_train and transforming them
X_test_scaled = scaler.transform(X_test) # transforming X_test. DO NOT FIT THEM!

# Visualizing data after scaling
print(f"\n-- AFTER SCALING -- X_train:\n{X_train_scaled[:5]}")
print(f"\n-- AFTER SCALING -- y_train:\n{y_train[:5]}")
print(f"\n-- AFTER SCALING -- X_test:\n{X_test_scaled[:5]}")
print(f"\n-- AFTER SCALING -- y_test:\n{y_test[:5]}")

# Modello di regressione lineare
model = LinearRegression()
model.fit(X_train_scaled, y_train)

#coefficiente del modello
coeff_df = pd.DataFrame(model.coef_, X.columns, columns=['Coefficient'])
print(coeff_df)

# Predizioni
y_pred = model.predict(X_test_scaled)

# Valutazione del modello
print('MSE:', mean_squared_error(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))
print('RMSE:', math.sqrt(mean_squared_error(y_test, y_pred)))

# residuals = y_test - model.predict(X_test)
# plt.figure(figsize=(8,6))
# sns.histplot(residuals, bins=30, kde=True)
# plt.xlabel("Errore della previsione")
# plt.ylabel("Frequenza")
# plt.title("Distribuzione degli errori della regressione")
# plt.show()
#
# 
#
#
# #sns.pairplot(df,diag_kind='kde')



