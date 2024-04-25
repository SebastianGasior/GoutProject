import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import joblib

# Load the processed dataset
df = pd.read_excel('processed_dataset.xlsx')

# features and target variable
X_reg = df[['Total_Purines_per_100g']]  # Example features; ensure no data leakage
y_reg = df['Uric_acid_per_100g']  

# Split the data into training and test sets
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
linear_reg_model = LinearRegression()
linear_reg_model.fit(X_train_reg, y_train_reg)

# Predict on the test set
y_pred_reg = linear_reg_model.predict(X_test_reg)

# Evaluate the regression model
mse = mean_squared_error(y_test_reg, y_pred_reg)
r2 = r2_score(y_test_reg, y_pred_reg)

print(f"Linear Regression MSE: {mse}, R2: {r2}")

# Initialize the Linear Regression model
linear_reg_model = LinearRegression()

# Perform k-fold cross-validation
cv_scores = cross_val_score(linear_reg_model, X_reg, y_reg, cv=10)  # cv is the number of folds

# Calculate the mean and standard deviation of the cross-validation scores
cv_mean = cv_scores.mean()
cv_std = cv_scores.std()

print(f'Linear Regression - CV Mean: {cv_mean}, CV Std: {cv_std}')

plt.figure(figsize=(10, 6))
plt.scatter(y_test_reg, y_pred_reg, alpha=0.5)
plt.plot(y_test_reg, y_test_reg, color='red')  # This line represents the perfect predictions
plt.title('Actual vs Predicted Uric Acid Content')
plt.xlabel('Actual Uric Acid per 100g')
plt.ylabel('Predicted Uric Acid per 100g')
plt.grid(True)
plt.show()

joblib.dump(linear_reg_model, 'Model_Development_RegressionModel.pkl')



