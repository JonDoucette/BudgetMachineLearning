import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib

def train_model(data):
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
    pipeline_vendor = Pipeline([
        ('tfidf', TfidfVectorizer()),  # For text vectorization
        ('clf', RandomForestClassifier())
    ])

    pipeline_category = Pipeline([
        ('tfidf', TfidfVectorizer()),  # Vectorize the 'description/name' text
        ('clf', RandomForestClassifier())
    ])

    # Train the model
    pipeline_vendor.fit(X_train['Description'], y_train_vendor)
    pipeline_category.fit(X_train['Description'], y_train_category)

    # Evaluate the model
    y_pred_vendor = pipeline_vendor.predict(X_test['Description'])
    print("Vendor Prediction Accuracy:", accuracy_score(y_test_vendor, y_pred_vendor))

    y_pred_category = pipeline_category.predict(X_test['Description'])
    print("Category Prediction Accuracy:", accuracy_score(y_test_category, y_pred_category))

    joblib.dump(pipeline_vendor, 'vendor_prediction_model.pkl')
    joblib.dump(pipeline_category, 'category_prediction_model.pkl')