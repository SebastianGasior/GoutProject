import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import joblib

# Load the processed dataset
df = pd.read_excel('processed_dataset.xlsx')

# As 'Food_Part' is not applicable in all cases, it can be dropped if it does not vary
# If 'Food_Part' varies and has relevant information, you should encode it instead
df.drop('Food_Part', axis=1, inplace=True)

# Encode the 'Foodstuffs' column if it's categorical
encoder = LabelEncoder()
df['Foodstuffs_encoded'] = encoder.fit_transform(df['Foodstuffs'])

# Prepare the data for modeling
X = df[['Foodstuffs_encoded', 'Total_Purines_per_100g', 'Uric_acid_per_100g']]  # Features
y = df['Classified_Group']  # Target

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the RandomForestClassifier
model = RandomForestClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))



# Initialize the RandomForestClassifier
rf_classifier = RandomForestClassifier(random_state=42)

# Perform k-fold cross-validation
cv_scores = cross_val_score(rf_classifier, X, y, cv=10, scoring='accuracy')  # cv is the number of folds

# Calculate the mean and standard deviation of the cross-validation scores
cv_mean = cv_scores.mean()
cv_std = cv_scores.std()

print(f'Random Forest Classifier - CV Mean: {cv_mean}, CV Std: {cv_std}')

# Visualize the feature importances
feature_importances = pd.Series(model.feature_importances_, index=X_train.columns)
sns.barplot(x=feature_importances, y=feature_importances.index)
plt.title('Feature Importances')
plt.show()

# Visualize the confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='g', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Visualize the cross-validation scores
sns.boxplot(x=cv_scores)
plt.title('Cross-validation Score Distribution')
plt.xlabel('Accuracy')
plt.show()

joblib.dump(model, 'Model_Development_RandomForestClassifier.pkl')
# Save the LabelEncoder to a file
joblib.dump(encoder, 'label_encoder.pkl')
