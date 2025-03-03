import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carica il dataset
df = pd.read_csv('Insurance_cleaned.csv')


#  Analisi Fumo-Costo
# Assumiamo che la colonna 'smoker' contenga 'yes' o 'no'
plt.figure(figsize=(10, 6))
sns.boxplot(x='smoker', y='charges', data=df)
plt.title('Relazione tra Fumo e Costo della Polizza')
plt.xlabel('Fumatore (Sì/No)')
plt.ylabel('Costo della Polizza')
plt.show()

# Statistiche descrittive per fumatori vs non fumatori
smoker_stats = df.groupby('smoker')['charges'].describe()
print(smoker_stats)

# Calcolare la differenza media tra fumatori e non fumatori
mean_smoker_cost = df[df['smoker'] == 'yes']['charges'].mean()
mean_non_smoker_cost = df[df['smoker'] == 'no']['charges'].mean()
print(f'Costo medio per fumatori: {mean_smoker_cost}')
print(f'Costo medio per non fumatori: {mean_non_smoker_cost}')