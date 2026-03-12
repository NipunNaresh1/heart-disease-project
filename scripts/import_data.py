#!/usr/bin/env python3
"""
Manual Data Import Script for Heart Disease Analytics
This script helps process manually downloaded heart disease datasets
"""

import pandas as pd
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def process_manual_dataset(file_path):
    """
    Process manually downloaded heart disease dataset
    """
    if not os.path.exists(file_path):
        print(f"Dataset file not found: {file_path}")
        return None
    
    print(f"Processing dataset: {file_path}")
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"Successfully loaded with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            print("Failed to read dataset with any encoding")
            return None
        
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"Error processing dataset: {e}")
        return None

def standardize_columns(df):
    """
    Standardize column names to match our project structure
    """
    # Common column mappings from different datasets
    column_mappings = {
        # UCI Heart Disease Dataset variations
        'age': 'age',
        'sex': 'sex',
        'cp': 'cp', 
        'trestbps': 'trestbps',
        'chol': 'chol',
        'fbs': 'fbs',
        'restecg': 'restecg',
        'thalach': 'thalach',
        'exang': 'exang',
        'oldpeak': 'oldpeak',
        'slope': 'slope',
        'ca': 'ca',
        'thal': 'thal',
        'target': 'target',
        'condition': 'target',  # Some datasets use 'condition'
        'HeartDisease': 'target',  # Some datasets use 'HeartDisease'
        'num': 'target',  # Cleveland dataset uses 'num'
        
        # Alternative column names
        'Age': 'age',
        'Sex': 'sex',
        'ChestPainType': 'cp',
        'RestingBP': 'trestbps',
        'Cholesterol': 'chol',
        'FastingBS': 'fbs',
        'RestingECG': 'restecg',
        'MaxHR': 'thalach',
        'ExerciseAngina': 'exang',
        'Oldpeak': 'oldpeak',
        'ST_Slope': 'slope',
        
        # Other variations
        'gender': 'sex',
        'chest_pain_type': 'cp',
        'resting_blood_pressure': 'trestbps',
        'serum_cholesterol': 'chol',
        'fasting_blood_sugar': 'fbs',
        'resting_ecg_results': 'restecg',
        'max_heart_rate_achieved': 'thalach',
        'exercise_induced_angina': 'exang',
        'st_depression': 'oldpeak',
        'st_slope': 'slope',
        'major_vessels': 'ca',
        'thalassemia': 'thal',
        'heart_disease': 'target',
        'has_heart_disease': 'target',
    }
    
    # Apply column mapping
    df = df.rename(columns=column_mappings)
    
    # Ensure we have all required columns
    required_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                       'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    
    # Check which columns are missing
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Warning: Missing columns: {missing_columns}")
        
        # Try to add missing columns with default values
        for col in missing_columns:
            if col == 'target':
                df[col] = 0  # Default to no heart disease
            elif col in ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'slope', 'ca', 'thal']:
                df[col] = 0  # Default to 0 for missing numeric columns
            elif col == 'oldpeak':
                df[col] = 0.0  # Default to 0.0 for oldpeak
    
    # Select only required columns
    available_columns = [col for col in required_columns if col in df.columns]
    df = df[available_columns]
    
    return df

def clean_data(df):
    """
    Clean and validate the dataset
    """
    print("Cleaning and validating data...")
    
    # Remove rows with missing values
    initial_shape = df.shape[0]
    df = df.dropna()
    print(f"Removed {initial_shape - df.shape[0]} rows with missing values")
    
    # Remove duplicates
    initial_shape = df.shape[0]
    df = df.drop_duplicates()
    print(f"Removed {initial_shape - df.shape[0]} duplicate rows")
    
    # Validate data ranges
    print("Validating data ranges...")
    
    # Age validation
    age_mask = (df['age'] >= 0) & (df['age'] <= 120)
    invalid_age = df[~age_mask].shape[0]
    if invalid_age > 0:
        print(f"Warning: {invalid_age} rows with invalid age values")
        df = df[age_mask]
    
    # Cholesterol validation
    if 'chol' in df.columns:
        chol_mask = (df['chol'] >= 100) & (df['chol'] <= 600)
        invalid_chol = df[~chol_mask].shape[0]
        if invalid_chol > 0:
            print(f"Warning: {invalid_chol} rows with invalid cholesterol values")
            df = df[chol_mask]
    
    # Blood pressure validation
    if 'trestbps' in df.columns:
        bp_mask = (df['trestbps'] >= 80) & (df['trestbps'] <= 250)
        invalid_bp = df[~bp_mask].shape[0]
        if invalid_bp > 0:
            print(f"Warning: {invalid_bp} rows with invalid blood pressure values")
            df = df[bp_mask]
    
    # Ensure target is binary (0 or 1)
    if 'target' in df.columns:
        df['target'] = df['target'].astype(int)
        df['target'] = df['target'].clip(0, 1)
    
    print(f"Final dataset shape: {df.shape}")
    return df

def save_processed_data(df, output_path='dataset/heart_disease_kaggle.csv'):
    """
    Save processed data to standard format
    """
    if df is not None:
        # Create dataset directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")
        
        # Show dataset statistics
        print("\nDataset Statistics:")
        print(f"Total records: {len(df)}")
        print(f"Heart disease cases: {df['target'].sum()}")
        print(f"Heart disease prevalence: {(df['target'].sum() / len(df) * 100):.1f}%")
        print(f"Average age: {df['age'].mean():.1f}")
        print(f"Average cholesterol: {df['chol'].mean():.1f}")
        print(f"Average blood pressure: {df['trestbps'].mean():.1f}")
        
        return True
    return False

def update_flask_app():
    """
    Update Flask app to use the new dataset
    """
    flask_app_path = 'flask_app/app.py'
    
    if os.path.exists(flask_app_path):
        with open(flask_app_path, 'r') as f:
            content = f.read()
        
        # Update CSV path to use Kaggle data
        updated_content = content.replace(
            "CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset', 'heart_disease.csv')",
            "CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset', 'heart_disease_kaggle.csv')"
        )
        
        with open(flask_app_path, 'w') as f:
            f.write(updated_content)
        
        print("Flask app updated to use new dataset")
        return True
    
    return False

def main():
    """
    Main function for manual data import
    """
    print("=" * 60)
    print("HEART DISEASE ANALYTICS - MANUAL DATA IMPORT")
    print("=" * 60)
    
    # Look for common dataset file names
    possible_files = [
        'dataset/heart.csv',
        'dataset/heart_disease.csv',
        'dataset/heart_disease_uci.csv',
        'dataset/heart.csv',
        'dataset/heart_disease_data.csv',
        'dataset/cleveland.csv',
        'dataset/hungarian.csv',
        'dataset/switzerland.csv',
        'dataset/va.csv'
    ]
    
    dataset_file = None
    for file_path in possible_files:
        if os.path.exists(file_path):
            dataset_file = file_path
            break
    
    if not dataset_file:
        print("\nNo dataset file found. Please download a heart disease dataset and place it in the 'dataset/' folder.")
        print("\nPopular datasets to download:")
        print("1. UCI Heart Disease Dataset: https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset")
        print("2. Heart Failure Prediction: https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction")
        print("3. Heart Attack Analysis: https://www.kaggle.com/datasets/rashikrahmanpritom/heart-attack-analysis-prediction")
        print("\nAfter downloading, place the CSV file in the 'dataset/' folder and run this script again.")
        return
    
    print(f"\nFound dataset file: {dataset_file}")
    
    # Step 1: Load the dataset
    print("\nStep 1: Loading dataset...")
    df = process_manual_dataset(dataset_file)
    
    if df is None:
        print("Failed to load dataset")
        return
    
    # Step 2: Standardize columns
    print("\nStep 2: Standardizing columns...")
    df = standardize_columns(df)
    
    # Step 3: Clean data
    print("\nStep 3: Cleaning data...")
    df = clean_data(df)
    
    # Step 4: Save processed data
    print("\nStep 4: Saving processed data...")
    if save_processed_data(df):
        print("Data saved successfully!")
    else:
        print("Failed to save data")
        return
    
    # Step 5: Update Flask app
    print("\nStep 5: Updating Flask application...")
    if update_flask_app():
        print("Flask app updated successfully!")
    else:
        print("Failed to update Flask app")
    
    print("\n" + "=" * 60)
    print("MANUAL DATA IMPORT COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Restart the Flask application")
    print("2. Visit http://127.0.0.1:5000 to see the updated dashboard")
    print("3. The dashboard will now display the imported dataset data")

if __name__ == "__main__":
    main()
