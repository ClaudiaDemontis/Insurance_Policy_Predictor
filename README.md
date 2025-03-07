# Insurance Policy Predictor

Il progetto **Insurance Policy Predictor** ha lo scopo di analizzare e prevedere il costo delle polizze assicurative sanitarie utilizzando tecniche di analisi esplorativa e machine learning. Il dataset utilizzato è il **Medical Cost Personal Dataset** (`Insurance_modified.csv`), che contiene informazioni su vari fattori che influenzano il costo delle polizze assicurative, come età, sesso, BMI, numero di figli, fumatore/non fumatore, regione di residenza e costo della polizza.

## Team

Il progetto è stato realizzato da: **Aurora Betta, Claudia Demontis, Francesco Bassani, Maria Grazia Cioffi, Meryem Karim, Valentina Gesù**.

## Link notebook: https://colab.research.google.com/drive/1pBV-iv2ETY6kHSNv2TYoJxt-0uvBWECB?usp=sharing 

## Fasi del Progetto

1. **Analisi del dataset**: Pulizia dei dati, individuazione delle relazioni tra i campi e creazione di uno schema ER.
2. **Creazione del database**: Creazione di un modello relazionale SQL e caricamento dei dati nelle tabelle.
3. **Sviluppo di una web app** con Flask per eseguire operazioni CRUD (Create, Read, Update, Delete) sul database.
4. **Analisi esplorativa dei dati** utilizzando librerie come Pandas, NumPy e Matplotlib per analizzare i dati e individuare pattern.
5. **Applicazione di tecniche di Machine Learning** (Regressione Lineare e Polinomiale) per prevedere il costo delle polizze.
6. **Reportistica**: Creazione di report tramite Power BI, PyCharm e Google Collab.

## Struttura del Progetto

### File e Cartelle Principali

- **`Insurance_modified.csv`**: Il dataset originale fornito per il progetto.
- **`Insurance_cleaned.csv`**: Il dataset pulito e pronto per l'uso.
- **`create_tables.py`**: Script per la creazione delle tabelle nel database SQL.
- **`data.py`**: Script per il caricamento e la pulizia del dataset.
- **`funzioni_utili.py`**: Contiene funzioni utili per l'esecuzione di query SQL e la gestione del database.
- **`insert_clients.py`**: Script per l'inserimento dei dati dei clienti nel database.
- **`insert_personal_info.py`**: Script per l'inserimento delle informazioni personali dei clienti nel database.
- **`insert_policies.py`**: Script per l'inserimento delle polizze assicurative nel database.
- **`insert_regions.py`**: Script per l'inserimento delle regioni nel database.
- **`machine_learning.py`**: Script per l'analisi esplorativa dei dati e l'applicazione di modelli di Machine Learning.
- **`web_app_menu/`**: Cartella contenente l'applicazione Flask.
  - **`app.py`**: File principale dell'applicazione Flask.
  - **`templates/`**: Contiene i file HTML per l'interfaccia utente.
  - **`static/`**: Contiene file CSS, JavaScript e immagini per l'interfaccia utente.

### Database

Il database è strutturato in quattro tabelle principali:
1. **`Personal_Info`**: Contiene informazioni personali dei clienti (nome, cognome, anno di nascita, email).
2. **`Regions`**: Contiene informazioni sulle regioni (nome, popolazione, tasso di criminalità, tasso di disoccupazione, reddito medio, eventi meteorologici estremi).
3. **`Policies`**: Contiene informazioni sulle polizze assicurative (costo, data di inizio, data di scadenza, stato).
4. **`Clients`**: Contiene informazioni sui clienti (età, sesso, BMI, numero di figli, fumatore/non fumatore, regione di residenza, ID polizza).

### Web App

L'applicazione web è sviluppata utilizzando **Flask** e permette di:
- **Visualizzare i dati assicurativi** caricati da un file CSV.
- **Gestire i clienti**: Inserire, modificare, eliminare e cercare clienti.
- **Gestire le polizze**: Visualizzare e modificare le polizze assicurative.
- **Eseguire query** per estrarre informazioni specifiche dal database.

### Machine Learning

#### File Principali di Machine Learning

1. **`testPredict.py`**:
   - Carica il dataset `Insurance_cleaned.csv`.
   - Preprocessa i dati (scalatura e codifica delle variabili categoriche).
   - Addestra un modello di regressione lineare.
   - Valuta il modello utilizzando metriche come MSE, MAE e RMSE.
   - Permette di inserire manualmente un nuovo dato e prevedere il costo assicurativo.

2. **`uso_modello.py`**:
   - Carica un modello di regressione lineare pre-addestrato (`modello_regressione_lineare.pkl`) e il preprocessore (`preprocessor.pkl`).
   - Fa previsioni su nuovi dati inseriti manualmente.

3. **`machine_learning.py`**:
   - Esegue un'analisi esplorativa dei dati (EDA) con visualizzazioni.
   - Addestra modelli di regressione lineare e polinomiale.
   - Confronta le prestazioni dei modelli utilizzando RMSE.
   - Genera grafici per valutare la normalità dei residui e l'andamento dell'errore al variare del grado polinomiale.

#### Dettagli su Machine Learning

- **Analisi Esplorativa dei Dati (EDA)**:
  - Visualizza la distribuzione dei costi assicurativi (`charges`).
  - Mostra grafici di correlazione tra le variabili.
- **Preprocessing**:
  - Codifica one-hot delle variabili categoriche (`sex`, `smoker`, `region`).
  - Scalatura delle variabili numeriche (`age`, `bmi`, `children`).
- **Modelli Implementati**:
  - **Regressione Lineare**:
    - Addestramento e valutazione con metriche (MSE, MAE, RMSE).
  - **Regressione Polinomiale** (gradi 1-4):
    - Confronto delle prestazioni tramite RMSE.
    - Visualizzazione dell'errore (RMSE) al variare del grado polinomiale.
- **Visualizzazioni**:
  - Grafico della distribuzione dei costi assicurativi.
  - Q-Q plot per valutare la normalità dei residui.
  - Grafico RMSE vs grado polinomiale.




