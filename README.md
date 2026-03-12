# ❤️ Heart Disease Analytics Dashboard
A comprehensive end-to-end data analytics project that analyzes heart disease patient data and builds an interactive dashboard to identify major risk factors such as age, cholesterol, blood pressure, chest pain, and heart rate.

## 🎯 Project Overview

This project demonstrates a complete data analytics pipeline from raw data to interactive visualizations and web integration. It combines SQL analytics, Tableau visualizations, and Flask web development to create a professional healthcare analytics dashboard.

### Key Features

* 📊 **Comprehensive Data Analysis**: 50+ realistic patient records with 14 clinical attributes
* 🗄️ **SQL Database Integration**: Optimized database schema with 16+ analytical queries
* 📈 **Interactive Visualizations**: 8 core Tableau visualizations with dashboard and story
* 🌐 **Web Application**: Flask-based web dashboard with real-time analytics
* 📱 **Responsive Design**: Mobile-friendly interface with Bootstrap 5
* 🔍 **Risk Assessment**: Multi-factor risk analysis and correlation studies
* 📋 **Professional Documentation**: Complete project report and technical documentation

## 🏗️ Project Structure

heart-disease-analytics/
│
├── dataset/
│   └── heart_disease.csv
│
├── database/
│   └── create_table.sql
│
├── sql/
│   └── analytics_queries.sql
│
├── flask_app/
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── dashboard.html
│
├── tableau/
│   └── tableau_visualization_plan.md
│
├── documentation/
│   └── project_report.md
│
└── README.md

## 🚀 Quick Start

### Prerequisites

* Python 3.9 or higher
* Node.js 14+
* Tableau Desktop
* Git

### Installation

1. Clone the repository

git clone https://github.com/yourusername/heart-disease-analytics.git
cd heart-disease-analytics

2. Set up Python environment

python -m venv venv
source venv/bin/activate

Windows:

venv\Scripts\activate

3. Install dependencies

cd flask_app
pip install -r requirements.txt

4. Run the Flask application

python app.py

5. Open in browser

http://localhost:5000

## 📊 Dataset Description

The dataset contains 14 clinical attributes including:

* Age
* Gender
* Chest Pain Type
* Blood Pressure
* Cholesterol
* Heart Rate
* ECG Results
* Exercise Induced Angina
* Heart Disease Target

## 📈 SQL Analytics

Includes multiple SQL queries like:

* Age group analysis
* Cholesterol vs heart disease
* Gender distribution
* Risk factor correlation

Example:

SELECT
CASE
WHEN age < 30 THEN 'Under 30'
WHEN age BETWEEN 30 AND 39 THEN '30-39'
WHEN age BETWEEN 40 AND 49 THEN '40-49'
WHEN age BETWEEN 50 AND 59 THEN '50-59'
WHEN age BETWEEN 60 AND 69 THEN '60-69'
ELSE '70+'
END as age_group,
COUNT(*) as total_patients
FROM heart_disease
GROUP BY age_group

## 📊 Tableau Visualizations

The project includes 8 visualizations:

1. Age Distribution
2. Gender Distribution
3. Cholesterol vs Heart Disease
4. Chest Pain Type Analysis
5. Heart Rate Distribution
6. Blood Pressure Trends
7. Risk Factor Heatmap
8. Age vs Cholesterol Scatter Plot

## 🌐 Flask Web Application

Features:

* Real-time analytics
* Interactive charts
* REST API endpoints
* Mobile responsive design

Example APIs:

/api/overview
/api/gender_distribution
/api/age_distribution
/api/cholesterol_analysis

## 🛠️ Technologies Used

Backend

* Python
* Flask
* SQLAlchemy
* SQLite

Data Analysis

* SQL
* Pandas

Visualization

* Tableau
* Chart.js

Frontend

* HTML
* Bootstrap
* JavaScript

## 📌 Future Improvements

* Machine learning heart disease prediction
* Larger medical datasets
* Real-time health monitoring
* Integration with hospital systems

## 📄 License

MIT License

## 🙏 Acknowledgments

* UCI Machine Learning Repository
* Tableau Community
* Flask Community

Built with ❤️ by Nipun, Kashish, Kartik, and Disha
