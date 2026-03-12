"""
Utility functions for the Heart Disease Analytics Dashboard.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def load_dataset(csv_path: Path) -> pd.DataFrame:
    """
    Load heart disease dataset from CSV file.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Loaded DataFrame
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        pd.errors.EmptyDataError: If the CSV file is empty
    """
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found: {csv_path}")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"Dataset file is empty: {csv_path}")
    except Exception as e:
        raise Exception(f"Error loading dataset: {str(e)}")

def validate_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Validate and clean the heart disease dataset.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Tuple of (cleaned DataFrame, validation report)
    """
    validation_report = {
        'original_shape': df.shape[0],
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': df.duplicated().sum(),
        'data_types': df.dtypes.to_dict(),
        'validation_errors': []
    }
    
    # Make a copy to avoid modifying original
    df_clean = df.copy()
    
    # Check required columns
    required_columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        validation_report['validation_errors'].append(f"Missing columns: {missing_columns}")
        # Add missing columns with default values
        for col in missing_columns:
            df_clean[col] = 0
    
    # Remove rows with missing values
    initial_rows = len(df_clean)
    df_clean = df_clean.dropna()
    removed_missing = initial_rows - len(df_clean)
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    removed_duplicates = initial_rows - len(df_clean) - removed_missing
    
    # Validate data ranges
    range_errors = []
    
    # Age validation
    if 'age' in df_clean.columns:
        invalid_age = df_clean[(df_clean['age'] < 0) | (df_clean['age'] > 120)].index
        if len(invalid_age) > 0:
            range_errors.append(f"Invalid age values: {len(invalid_age)} records")
            df_clean = df_clean.drop(invalid_age)
    
    # Cholesterol validation
    if 'chol' in df_clean.columns:
        invalid_chol = df_clean[(df_clean['chol'] < 100) | (df_clean['chol'] > 600)].index
        if len(invalid_chol) > 0:
            range_errors.append(f"Invalid cholesterol values: {len(invalid_chol)} records")
            df_clean = df_clean.drop(invalid_chol)
    
    # Blood pressure validation
    if 'trestbps' in df_clean.columns:
        invalid_bp = df_clean[(df_clean['trestbps'] < 80) | (df_clean['trestbps'] > 250)].index
        if len(invalid_bp) > 0:
            range_errors.append(f"Invalid blood pressure values: {len(invalid_bp)} records")
            df_clean = df_clean.drop(invalid_bp)
    
    # Ensure target is binary
    if 'target' in df_clean.columns:
        df_clean['target'] = df_clean['target'].astype(int)
        df_clean['target'] = df_clean['target'].clip(0, 1)
    
    validation_report.update({
        'final_shape': df_clean.shape[0],
        'removed_missing': removed_missing,
        'removed_duplicates': removed_duplicates,
        'range_errors': range_errors,
        'validation_errors': validation_report['validation_errors'] + range_errors
    })
    
    return df_clean, validation_report

def calculate_age_groups(age_series: pd.Series) -> pd.Series:
    """
    Calculate age groups for analysis.
    
    Args:
        age_series: Series of ages
        
    Returns:
        Series of age groups
    """
    return pd.cut(
        age_series,
        bins=[0, 30, 40, 50, 60, 70, 120],
        labels=['Under 30', '30-39', '40-49', '50-59', '60-69', '70+'],
        right=False
    )

def calculate_risk_factors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate risk factors for each patient.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with additional risk factor columns
    """
    df_risk = df.copy()
    
    # High cholesterol risk
    df_risk['high_chol_risk'] = (df_risk['chol'] > 240).astype(int)
    
    # High blood pressure risk
    df_risk['high_bp_risk'] = (df_risk['trestbps'] > 140).astype(int)
    
    # Age risk
    df_risk['age_risk'] = (df_risk['age'] > 55).astype(int)
    
    # Low heart rate risk
    df_risk['low_hr_risk'] = (df_risk['thalach'] < 120).astype(int)
    
    # Overall risk score
    df_risk['risk_score'] = (
        df_risk['high_chol_risk'] + 
        df_risk['high_bp_risk'] + 
        df_risk['age_risk'] + 
        df_risk['low_hr_risk']
    )
    
    # Risk category
    def categorize_risk(score):
        if score >= 3:
            return 'High Risk'
        elif score >= 2:
            return 'Medium Risk'
        else:
            return 'Low Risk'
    
    df_risk['risk_category'] = df_risk['risk_score'].apply(categorize_risk)
    
    return df_risk

def generate_summary_statistics(df: pd.DataFrame) -> Dict:
    """
    Generate summary statistics for the dataset.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary of summary statistics
    """
    stats = {
        'total_patients': len(df),
        'heart_disease_cases': df['target'].sum(),
        'heart_disease_percentage': (df['target'].sum() / len(df) * 100),
        'age_stats': {
            'mean': df['age'].mean(),
            'std': df['age'].std(),
            'min': df['age'].min(),
            'max': df['age'].max()
        },
        'cholesterol_stats': {
            'mean': df['chol'].mean(),
            'std': df['chol'].std(),
            'min': df['chol'].min(),
            'max': df['chol'].max()
        },
        'blood_pressure_stats': {
            'mean': df['trestbps'].mean(),
            'std': df['trestbps'].std(),
            'min': df['trestbps'].min(),
            'max': df['trestbps'].max()
        },
        'gender_distribution': df['sex'].value_counts().to_dict(),
        'chest_pain_distribution': df['cp'].value_counts().to_dict()
    }
    
    return stats

def format_number(value: float, decimal_places: int = 2) -> str:
    """
    Format a number for display.
    
    Args:
        value: Number to format
        decimal_places: Number of decimal places
        
    Returns:
        Formatted string
    """
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimal_places}f}"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if denominator is zero
        
    Returns:
        Result of division or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator
