# Import section
import pandas as pd  # Importing the pandas library for data manipulation

# Dataset uploading
df = pd.read_csv("Insurance_modified.csv")  # Loading the dataset into a pandas DataFrame

# Counting the number of NaN values in each column
print(f"\nNumber  of NaN values per column:\n{df.isna().sum()}")  # Displaying the count of missing values

# Removing rows with NaN values
df_modified = df.dropna()  # Creating a new DataFrame without missing values

# Printing the modified DataFrame
print(df_modified)  # Displaying the cleaned dataset

df_modified.to_csv('Insurance_cleaned.csv', index=False)