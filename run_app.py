"""
Simple Heart Disease Analytics Dashboard
Quick start version for immediate testing
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import sqlite3
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Database configuration
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'data' / 'heart_disease.db'
CSV_PATH = BASE_DIR / 'dataset' / 'heart_disease.csv'

def init_database():
    """Initialize SQLite database with CSV data"""
    if not DB_PATH.exists():
        # Create data directory if it doesn't exist
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Read CSV data
            df = pd.read_csv(CSV_PATH)
            print(f"Loaded {len(df)} records from CSV")
            
            # Connect to SQLite database
            conn = sqlite3.connect(str(DB_PATH))
            
            # Create table and insert data
            df.to_sql('heart_disease', conn, if_exists='replace', index=False)
            
            conn.close()
            print("Database initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing database: {e}")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query):
    """Execute SQL query and return results"""
    conn = get_db_connection()
    try:
        result = conn.execute(query).fetchall()
        return [dict(row) for row in result]
    finally:
        conn.close()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/overview')
def get_overview():
    """Get overview statistics"""
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
    """Get gender distribution data"""
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
    """Get age distribution data"""
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

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("Starting Heart Disease Analytics Dashboard...")
    
    # Initialize database
    init_database()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
