"""
Heart Disease Analytics Dashboard - Main Flask Application

This application provides a comprehensive web interface for analyzing heart disease data
with interactive visualizations and real-time analytics.

Author: Healthcare Analytics Team
Version: 1.0.0
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, jsonify, request
import pandas as pd
import sqlite3

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from config import config
from utils import (
    load_dataset, validate_data, calculate_age_groups, 
    calculate_risk_factors, generate_summary_statistics
)

# Initialize Flask app
def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    init_database(app)
    
    # Register routes
    register_routes(app)
    
    return app

def init_database(app):
    """Initialize SQLite database with CSV data."""
    data_dir = app.config.get('DATABASE_PATH', Path(__file__).parent.parent / 'data' / 'heart_disease.db')
    csv_path = app.config.get('CSV_PATH', Path(__file__).parent.parent / 'dataset' / 'heart_disease.csv')
    
    # Create data directory if it doesn't exist
    data_dir.parent.mkdir(parents=True, exist_ok=True)
    
    if not data_dir.exists():
        print(f"Initializing database from: {csv_path}")
        
        try:
            # Load and validate data
            df = load_dataset(csv_path)
            df_clean, validation_report = validate_data(df)
            
            print(f"Data validation completed:")
            print(f"  - Original records: {validation_report['original_shape']}")
            print(f"  - Final records: {validation_report['final_shape']}")
            print(f"  - Removed missing: {validation_report['removed_missing']}")
            print(f"  - Removed duplicates: {validation_report['removed_duplicates']}")
            
            # Connect to SQLite database
            conn = sqlite3.connect(str(data_dir))
            
            # Create table and insert data
            df_clean.to_sql('heart_disease', conn, if_exists='replace', index=False)
            
            conn.close()
            print("Database initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            # Create empty database with structure
            conn = sqlite3.connect(str(data_dir))
            conn.execute('''
                CREATE TABLE IF NOT EXISTS heart_disease (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    age INTEGER NOT NULL,
                    sex INTEGER NOT NULL,
                    cp INTEGER NOT NULL,
                    trestbps INTEGER NOT NULL,
                    chol INTEGER NOT NULL,
                    fbs INTEGER NOT NULL,
                    restecg INTEGER NOT NULL,
                    thalach INTEGER NOT NULL,
                    exang INTEGER NOT NULL,
                    oldpeak REAL NOT NULL,
                    slope INTEGER NOT NULL,
                    ca INTEGER NOT NULL,
                    thal INTEGER NOT NULL,
                    target INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.close()

def get_db_connection():
    """Get database connection with proper error handling."""
    db_path = Path(__file__).parent.parent / 'data' / 'heart_disease.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=None):
    """Execute SQL query and return results with error handling."""
    conn = get_db_connection()
    try:
        if params:
            result = conn.execute(query, params).fetchall()
        else:
            result = conn.execute(query).fetchall()
        return [dict(row) for row in result]
    except Exception as e:
        print(f"Database query error: {e}")
        return []
    finally:
        conn.close()

def register_routes(app):
    """Register all application routes."""
    
    @app.route('/')
    def dashboard():
        """Main dashboard page."""
        return render_template('dashboard.html')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })

    @app.route('/api/overview')
    def get_overview():
        """Get overview statistics for the dashboard."""
        try:
            queries = {
                'total_patients': "SELECT COUNT(*) as count FROM heart_disease",
                'avg_age': "SELECT ROUND(AVG(age), 1) as avg_age FROM heart_disease",
                'avg_cholesterol': "SELECT ROUND(AVG(chol), 1) as avg_chol FROM heart_disease",
                'heart_disease_percentage': """
                    SELECT ROUND((SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 1) as percentage 
                    FROM heart_disease
                """
            }
            
            results = {}
            for key, query in queries.items():
                data = execute_query(query)
                results[key] = data[0] if data else {}
            
            return jsonify(results)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/gender_distribution')
    def get_gender_distribution():
        """Get gender distribution data."""
        try:
            query = """
                SELECT 
                    CASE 
                        WHEN sex = 1 THEN 'Male'
                        WHEN sex = 0 THEN 'Female'
                    END as gender,
                    COUNT(*) as count,
                    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases
                FROM heart_disease
                GROUP BY sex
            """
            return jsonify(execute_query(query))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/age_distribution')
    def get_age_distribution():
        """Get age distribution data."""
        try:
            query = """
                SELECT 
                    CASE 
                        WHEN age < 30 THEN 'Under 30'
                        WHEN age BETWEEN 30 AND 39 THEN '30-39'
                        WHEN age BETWEEN 40 AND 49 THEN '40-49'
                        WHEN age BETWEEN 50 AND 59 THEN '50-59'
                        WHEN age BETWEEN 60 AND 69 THEN '60-69'
                        ELSE '70+'
                    END as age_group,
                    COUNT(*) as count,
                    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases
                FROM heart_disease
                GROUP BY 
                    CASE 
                        WHEN age < 30 THEN 'Under 30'
                        WHEN age BETWEEN 30 AND 39 THEN '30-39'
                        WHEN age BETWEEN 40 AND 49 THEN '40-49'
                        WHEN age BETWEEN 50 AND 59 THEN '50-59'
                        WHEN age BETWEEN 60 AND 69 THEN '60-69'
                        ELSE '70+'
                    END
                ORDER BY age_group
            """
            return jsonify(execute_query(query))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/chest_pain_analysis')
    def get_chest_pain_analysis():
        """Get chest pain type analysis."""
        try:
            query = """
                SELECT 
                    CASE 
                        WHEN cp = 1 THEN 'Typical Angina'
                        WHEN cp = 2 THEN 'Atypical Angina'
                        WHEN cp = 3 THEN 'Non-anginal Pain'
                        WHEN cp = 4 THEN 'Asymptomatic'
                    END as chest_pain_type,
                    COUNT(*) as count,
                    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases,
                    ROUND((SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 1) as percentage
                FROM heart_disease
                GROUP BY cp
                ORDER BY count DESC
            """
            return jsonify(execute_query(query))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/cholesterol_analysis')
    def get_cholesterol_analysis():
        """Get cholesterol level analysis."""
        try:
            query = """
                SELECT 
                    CASE 
                        WHEN chol < 200 THEN 'Normal (<200)'
                        WHEN chol BETWEEN 200 AND 239 THEN 'Borderline High (200-239)'
                        WHEN chol >= 240 THEN 'High (>=240)'
                    END as cholesterol_level,
                    COUNT(*) as count,
                    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases,
                    ROUND(AVG(chol), 1) as avg_cholesterol
                FROM heart_disease
                GROUP BY 
                    CASE 
                        WHEN chol < 200 THEN 'Normal (<200)'
                        WHEN chol BETWEEN 200 AND 239 THEN 'Borderline High (200-239)'
                        WHEN chol >= 240 THEN 'High (>=240)'
                    END
                ORDER BY avg_cholesterol
            """
            return jsonify(execute_query(query))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/blood_pressure_analysis')
    def get_blood_pressure_analysis():
        """Get blood pressure analysis."""
        try:
            query = """
                SELECT 
                    CASE 
                        WHEN trestbps < 120 THEN 'Normal (<120)'
                        WHEN trestbps BETWEEN 120 AND 129 THEN 'Elevated (120-129)'
                        WHEN trestbps BETWEEN 130 AND 139 THEN 'High Stage 1 (130-139)'
                        WHEN trestbps >= 140 THEN 'High Stage 2+ (>=140)'
                    END as bp_category,
                    COUNT(*) as count,
                    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases,
                    ROUND(AVG(trestbps), 1) as avg_bp
                FROM heart_disease
                GROUP BY 
                    CASE 
                        WHEN trestbps < 120 THEN 'Normal (<120)'
                        WHEN trestbps BETWEEN 120 AND 129 THEN 'Elevated (120-129)'
                        WHEN trestbps BETWEEN 130 AND 139 THEN 'High Stage 1 (130-139)'
                        WHEN trestbps >= 140 THEN 'High Stage 2+ (>=140)'
                    END
                ORDER BY avg_bp
            """
            return jsonify(execute_query(query))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/heart_rate_analysis')
    def get_heart_rate_analysis():
        """Get heart rate analysis."""
        try:
            query = """
                SELECT 
                    ROUND(AVG(thalach), 1) as avg_max_heart_rate,
                    MIN(thalach) as min_heart_rate,
                    MAX(thalach) as max_heart_rate,
                    ROUND(STDDEV(thalach), 1) as std_dev_heart_rate
                FROM heart_disease
            """
            data = execute_query(query)
            return jsonify(data[0] if data else {})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/risk_factors')
    def get_risk_factors():
        """Get comprehensive risk factor analysis."""
        try:
            query = """
                SELECT 
                    'Age' as factor,
                    ROUND(AVG(CASE WHEN target = 1 THEN age END), 1) as avg_with_disease,
                    ROUND(AVG(CASE WHEN target = 0 THEN age END), 1) as avg_without_disease
                FROM heart_disease
                UNION ALL
                SELECT 
                    'Cholesterol' as factor,
                    ROUND(AVG(CASE WHEN target = 1 THEN chol END), 1) as avg_with_disease,
                    ROUND(AVG(CASE WHEN target = 0 THEN chol END), 1) as avg_without_disease
                FROM heart_disease
                UNION ALL
                SELECT 
                    'Blood Pressure' as factor,
                    ROUND(AVG(CASE WHEN target = 1 THEN trestbps END), 1) as avg_with_disease,
                    ROUND(AVG(CASE WHEN target = 0 THEN trestbps END), 1) as avg_without_disease
                FROM heart_disease
                UNION ALL
                SELECT 
                    'Max Heart Rate' as factor,
                    ROUND(AVG(CASE WHEN target = 1 THEN thalach END), 1) as avg_with_disease,
                    ROUND(AVG(CASE WHEN target = 0 THEN thalach END), 1) as avg_without_disease
                FROM heart_disease
            """
            return jsonify(execute_query(query))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Create application instance
app = create_app()

def main():
    """Main entry point for the application."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Heart Disease Analytics Dashboard')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--config', default='development', help='Configuration to use')
    
    args = parser.parse_args()
    
    print(f"Starting Heart Disease Analytics Dashboard...")
    print(f"Configuration: {args.config}")
    print(f"Debug mode: {args.debug}")
    print(f"Server: http://{args.host}:{args.port}")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()
