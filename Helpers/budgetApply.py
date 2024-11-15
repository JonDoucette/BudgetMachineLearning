import pandas as pd
import joblib
import numpy as np



# Function to add predictions to new data
def add_predictions_to_excel(input_file, output_file, confidence_threshold=0.8):
    # Load the new data
    new_data = pd.read_excel(input_file)

    # Load the trained models
    pipeline_category = joblib.load('Helpers/category_prediction_model.pkl')
    pipeline_vendor = joblib.load('Helpers/vendor_prediction_model.pkl')

    # Preprocess: Adding necessary columns from the date if not already present
    if 'month' not in new_data.columns:
        new_data['month'] = pd.to_datetime(new_data['Date']).dt.month
    if 'day_of_week' not in new_data.columns:
        new_data['day_of_week'] = pd.to_datetime(new_data['Date']).dt.dayofweek
    
    # Predict Vendor
    vendor_probs = pipeline_vendor.predict_proba(new_data['Description'])
    vendor_predictions = pipeline_vendor.predict(new_data['Description'])
    vendor_confidence = np.max(vendor_probs, axis=1)  # Max probability for the predicted class

    new_data['Predicted_Vendor'] = np.where(vendor_confidence >= confidence_threshold, 
                                            vendor_predictions, 
                                            None)
    new_data['Vendor_Confidence'] = vendor_confidence

    # Predict Category
    category_probs = pipeline_category.predict_proba(new_data['Description'])
    category_predictions = pipeline_category.predict(new_data['Description'])
    category_confidence = np.max(category_probs, axis=1)  # Max probability for the predicted class
    
    new_data['Predicted_Category'] = np.where(category_confidence >= confidence_threshold, 
                                              category_predictions, 
                                              None)
    new_data['Category_Confidence'] = category_confidence

    
    formatted_data = new_data.drop(columns=['month', 'day_of_week', 'Vendor_Confidence', 'Category_Confidence'])
    output_file = 'Formatted_' + output_file
    formatted_data.to_excel(output_file, index=False)
    print(f"Formatted Predictions saved to {output_file}")