# 1. Analisi Età-Costo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carica il dataset
df = pd.read_csv('Insurance_cleaned.csv')

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