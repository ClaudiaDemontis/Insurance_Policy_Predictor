#Import section
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.compose import ColumnTransformer
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler

def pipe_line(features, y, test_size = 0.2):
    # SPLIT THIS NEW POLY DATA SET

    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.3, random_state=101)

    # Selezione delle colonne numeriche (escludendo quelle categoriche)
    colonne_numeriche = [i for i in range(X_train.shape[1] - 3)] # Creazione del ColumnTransformer per scalare solo le colonne numeriche
    preprocessor = ColumnTransformer(
        [('scaler', StandardScaler(), colonne_numeriche)  # Applica lo scaling solo alle colonne numeriche
         ], remainder='passthrough')  # Mantiene inalterate le altre colonne (variabili dummy) #

    # Feature scaling
    # we are going to scale ONLY the features (i.e. the X) and NOT the y!
    X_train_scaled = preprocessor.fit_transform(X_train)  # fitting to X_train and transforming them
    X_test_scaled = preprocessor.transform(X_test)  # transforming X_test. DO NOT FIT THEM!

    X_train_scaled = pd.DataFrame(X_train_scaled, columns=colonne_numeriche + [col for col in range(X_train.shape[1] - 3, X_train.shape[1])])
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=colonne_numeriche + [col for col in range(X_train.shape[1] - 3, X_train.shape[1])])

    # TRAIN ON THIS NEW POLY SET
    model = LinearRegression(fit_intercept=True)
    model.fit(X_train_scaled, y_train)
    import numpy as np
    # Esempio di input
    eta = 35
    sesso = 'male'
    bmi = 28.5
    children = 2
    smoker = 'no'
    region = 'northwest'

    # Conversione delle categoriche
    sesso_num = 1 if sesso == 'male' else 0
    smoker_num = 1 if smoker == 'yes' else 0

    # One-hot encoding manuale per region
    regioni = ['northeast', 'northwest', 'southeast', 'southwest']
    region_encoded = [1 if regione == region else 0 for regione in regioni]

    # Composizione finale del dato in input
    nuovi_dati = np.array([[eta, sesso_num, bmi, children, smoker_num] + region_encoded])

    # Scala il dato se hai usato uno scaler (ad esempio StandardScaler)
    scaler = StandardScaler()
    nuovi_dati_scaled = scaler.transform(nuovi_dati)

    # Previsione
    previsione = model.predict(nuovi_dati_scaled)

    print(f"La previsione dei charges è: {previsione[0]:.2f}")

    # PREDICT ON BOTH TRAIN AND TEST
    # train_pred = model.predict(X_train_scaled)
    # test_pred = model.predict(X_test_scaled)
    #
    # # Calculate Errors
    #
    # # Errors on Train Set
    # train_RMSE = math.sqrt(mean_squared_error(y_train, train_pred))
    #
    # # Errors on Test Set
    # test_RMSE = math.sqrt(mean_squared_error(y_test, test_pred))
    #
    # return {
    #     "X_train_scaled": X_train_scaled ,
    #     "X_test_scaled" : X_test_scaled,
    #     "model": model,
    #     "train_pred": train_pred,
    #     "test_pred": test_pred,
    #     "train_RMSE":train_RMSE,
    #     "test_RMSE": test_RMSE,
    #     "y_train" : y_train,
    #     "y_test": y_test
    #
    # }

# Caricamento e esplorazione del dataset
df = pd.read_csv('Insurance_cleaned.csv')

#Matrice di confusione
sns.pairplot(df,diag_kind='kde')
plt.show()

# Esplorazione dei primi record del dataset
print(df.head())

# Stampa a video delle colonne
print(df.columns)

# Statistiche descrittive
print(df.describe())

# Visualizzazione dei dati
# Grafico della distribuzione del costo
sns.histplot(df['charges'], kde=True)
plt.title('Distribuzione del costo delle polizze')
plt.show()

#Conversione delle variabili non numeriche
df = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=True)

# Costruzione del modello di regressione lineare
# Selezione delle variabili indipendenti e dipendenti
X = df.drop(columns=['charges'])
y = df['charges']

results = pipe_line(X,y)

# # Valutazione del modello
# print("\nQueste sono le metriche di una regressione lineare")
# print('MSE:', mean_squared_error(results["y_test"], results["test_pred"]))
# print('MAE:', mean_absolute_error(results["y_test"], results["test_pred"]))
# print('RMSE:', math.sqrt(mean_squared_error(results["y_test"], results["test_pred"])))
# print("Media della colonna charges: ",df["charges"].mean())
#
# # Calcola i residui (errori della regressione)
# residuals = results["y_test"] - results["test_pred"]
#
# # Q-Q Plot per verificare la normalità dei residui
# plt.figure(figsize=(8,6))
# stats.probplot(residuals, dist="norm", plot=plt)  # Confronta con distribuzione normale
# plt.title("Q-Q Plot dei Residui di lineare")
# plt.show()
#
# # CREATE POLY DATA SET FOR DEGREE "2"
# polynomial_converter = PolynomialFeatures(degree=2, include_bias=False)
# poly_features = polynomial_converter.fit_transform(X)
#
# # SPLIT THIS NEW POLY DATA SET
# results = pipe_line(poly_features, y)
# print("\nQueste sono le metriche di una regressione polinomiale di grado 2")
# print('MSE:', mean_squared_error(results["y_test"], results["test_pred"]))
# print('MAE:', mean_absolute_error(results["y_test"], results["test_pred"]))
# print('RMSE:', math.sqrt(mean_squared_error(results["y_test"], results["test_pred"])))
# print("Media della colonna charges: ",df["charges"].mean())
#
# # Calcola i residui (errori della regressione)
# residuals = results["y_test"] - results["test_pred"]
#
# # Q-Q Plot per verificare la normalità dei residui
# plt.figure(figsize=(8,6))
# stats.probplot(residuals, dist="norm", plot=plt)  # Confronta con distribuzione normale
# plt.title("Q-Q Plot dei Residui di polinomiale di grado 2")
# plt.show()
#
# # TRAINING ERROR PER DEGREE
# train_rmse_errors = []
# # TEST ERROR PER DEGREE
# test_rmse_errors = []
#
# # Ciclo su diversi gradi polinomiali
# for d in range(1, 5):
#     # CREATE POLY DATA SET FOR DEGREE "d"
#     polynomial_converter = PolynomialFeatures(degree=d, include_bias=False)
#     poly_features = polynomial_converter.fit_transform(X)
#
#     # SPLIT THIS NEW POLY DATA SET
#     results = pipe_line(poly_features, y)
#
#     # Append errors to lists for plotting later
#     train_rmse_errors.append(results["train_RMSE"])
#     test_rmse_errors.append(results["test_RMSE"])
#
# # Plotting
# plt.plot(range(1, 5), train_rmse_errors, label='TRAIN')
# plt.plot(range(1, 5), test_rmse_errors, label='TEST')
# plt.xlabel("Polynomial Complexity (Degree)")
# plt.ylabel("RMSE")
# plt.legend()
# plt.title("RMSE vs Polynomial Degree")
# plt.show()
#



