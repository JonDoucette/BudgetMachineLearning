import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Load and preprocess data
data = pd.read_excel('Final - Complete Budget & Receipt Tracker.xlsx')
# Example of data preprocessing and feature engineering
data['month'] = pd.to_datetime(data['Date']).dt.month
data['day_of_week'] = pd.to_datetime(data['Date']).dt.dayofweek

# Splitting features and targets
X = data[['Description', 'Amount', 'month', 'day_of_week']]
y_vendor = data['Vendor']
y_category = data['Category']   

# Splitting data for vendor prediction
X_train, X_test, y_train_vendor, y_test_vendor = train_test_split(X, y_vendor, test_size=0.2, random_state=42)
X_train, X_test, y_train_category, y_test_category = train_test_split(X, y_category, test_size=0.2, random_state=42)

# Define a pipeline for vendor prediction using text vectorization and Random Forest

vendor_pipeline = Pipeline([
    ('preprocessor', ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(), 'Description'),  # Apply TF-IDF to text
            ('num', StandardScaler(), ['Amount'])  # Standard scale the numerical data
        ]
    )),
    ('clf', RandomForestClassifier())  # Train with a Random Forest
])

category_pipeline = Pipeline([
    ('preprocessor', ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(), 'Description'),  # Apply TF-IDF to text
            ('num', StandardScaler(), ['Amount'])  # Standard scale the numerical data
        ]
    )),
    ('clf', RandomForestClassifier())  # Train with a Random Forest
])


# Train the model
vendor_pipeline.fit(X_train, y_train_vendor)
category_pipeline.fit(X_train, y_train_category)

# Evaluate the model
y_pred_vendor = vendor_pipeline.predict(X_test)
print("Vendor Prediction Accuracy:", accuracy_score(y_test_vendor, y_pred_vendor))

y_pred_category = category_pipeline.predict(X_test)
print("Category Prediction Accuracy:", accuracy_score(y_test_category, y_pred_category))

joblib.dump(vendor_pipeline, 'vendor_prediction_model1.pkl')
joblib.dump(category_pipeline, 'category_prediction_model1.pkl')