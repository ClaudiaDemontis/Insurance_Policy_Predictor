# Import section
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
from sklearn.preprocessing import PolynomialFeatures

def pipe_line(features, y, test_size = 0.2):
    """
    Function to perform the training and evaluation pipeline for the model.
    """

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.3, random_state=101)

    # Selecting the numeric columns
    numeric_columns = [i for i in range(X_train.shape[1] - 3)]  # Consider the first columns as numeric
    preprocessor = ColumnTransformer(
        [('scaler', StandardScaler(), numeric_columns)], remainder='passthrough'
    )

    # Scaling the features
    X_train_scaled = preprocessor.fit_transform(X_train)  # Fitting on X_train
    X_test_scaled = preprocessor.transform(X_test)  # Only transforming X_test

    X_train_scaled = pd.DataFrame(X_train_scaled, columns=numeric_columns + [col for col in range(X_train.shape[1] - 3, X_train.shape[1])])
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=numeric_columns + [col for col in range(X_train.shape[1] - 3, X_train.shape[1])])

    # Training the linear regression model
    model = LinearRegression(fit_intercept=True)
    model.fit(X_train_scaled, y_train)

    # Predicting on both train and test sets
    train_pred = model.predict(X_train_scaled)
    test_pred = model.predict(X_test_scaled)

    # Calculating the errors
    train_RMSE = math.sqrt(mean_squared_error(y_train, train_pred))
    test_RMSE = math.sqrt(mean_squared_error(y_test, test_pred))

    return {
        "X_train_scaled": X_train_scaled,
        "X_test_scaled": X_test_scaled,
        "model": model,
        "train_pred": train_pred,
        "test_pred": test_pred,
        "train_RMSE": train_RMSE,
        "test_RMSE": test_RMSE,
        "y_train": y_train,
        "y_test": y_test
    }

# Loading and exploring the dataset
df = pd.read_csv('Insurance_cleaned.csv')

# Visualizing the pairplot to show relationships between features
sns.pairplot(df, diag_kind='kde')
plt.show()

# Exploring the first records of the dataset
print(df.head())

# Displaying the columns of the dataset
print(df.columns)

# Descriptive statistics
print(df.describe())

# Visualizing the distribution of the insurance costs (charges)
sns.histplot(df['charges'], kde=True)
plt.title('Distribution of Insurance Costs (Charges)')
plt.show()

# Converting categorical variables to numerical ones
df = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=True)

# Selecting the independent (features) and dependent (target) variables
X = df.drop(columns=['charges'])
y = df['charges']

# Running the pipeline for linear regression
results = pipe_line(X, y)

# Evaluating the linear regression model
print("\nThese are the metrics for linear regression")
print('MSE:', mean_squared_error(results["y_test"], results["test_pred"]))
print('MAE:', mean_absolute_error(results["y_test"], results["test_pred"]))
print('RMSE:', math.sqrt(mean_squared_error(results["y_test"], results["test_pred"])))
print("Mean of the 'charges' column:", df["charges"].mean())

# Calculating and visualizing the residuals (errors of the regression)
residuals = results["y_test"] - results["test_pred"]

# Q-Q Plot to check the normality of the residuals
plt.figure(figsize=(8,6))
stats.probplot(residuals, dist="norm", plot=plt)  # Comparing with normal distribution
plt.title("Q-Q Plot of Linear Regression Residuals")
plt.show()

# Creating the dataset with polynomial transformation of degree 2
polynomial_converter = PolynomialFeatures(degree=2, include_bias=False)
poly_features = polynomial_converter.fit_transform(X)

# Running the pipeline with the polynomial dataset
results = pipe_line(poly_features, y)

print("\nThese are the metrics for the polynomial regression of degree 2")
print('MSE:', mean_squared_error(results["y_test"], results["test_pred"]))
print('MAE:', mean_absolute_error(results["y_test"], results["test_pred"]))
print('RMSE:', math.sqrt(mean_squared_error(results["y_test"], results["test_pred"])))
print("Mean of the 'charges' column:", df["charges"].mean())

# Calculating and visualizing the residuals for the polynomial regression
residuals = results["y_test"] - results["test_pred"]
plt.figure(figsize=(8,6))
stats.probplot(residuals, dist="norm", plot=plt)
plt.title("Q-Q Plot of Polynomial Regression Degree 2 Residuals")
plt.show()

# Training error for different polynomial degrees
train_rmse_errors = []
test_rmse_errors = []

# Looping over different polynomial degrees
for d in range(1, 5):
    polynomial_converter = PolynomialFeatures(degree=d, include_bias=False)
    poly_features = polynomial_converter.fit_transform(X)

    results = pipe_line(poly_features, y)

    train_rmse_errors.append(results["train_RMSE"])
    test_rmse_errors.append(results["test_RMSE"])

# Plotting RMSE errors vs polynomial degree
plt.plot(range(1, 5), train_rmse_errors, label='TRAIN')
plt.plot(range(1, 5), test_rmse_errors, label='TEST')
plt.xlabel("Polynomial Complexity (Degree)")
plt.ylabel("RMSE")
plt.legend()
plt.title("RMSE vs Polynomial Degree")
plt.show()



