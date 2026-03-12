-- Heart Disease Analytics Queries
-- Comprehensive SQL analysis for heart disease dataset

-- 1. Total number of patients
SELECT COUNT(*) as total_patients 
FROM heart_disease;

-- 2. Average age of patients
SELECT 
    ROUND(AVG(age), 2) as average_age,
    MIN(age) as youngest_patient,
    MAX(age) as oldest_patient
FROM heart_disease;

-- 3. Average cholesterol levels
SELECT 
    ROUND(AVG(chol), 2) as average_cholesterol,
    MIN(chol) as min_cholesterol,
    MAX(chol) as max_cholesterol
FROM heart_disease;

-- 4. Heart disease count and percentage
SELECT 
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as patients_with_heart_disease,
    SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) as patients_without_heart_disease,
    ROUND((SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) as heart_disease_percentage
FROM heart_disease;

-- 5. Patients grouped by gender
SELECT 
    CASE 
        WHEN sex = 1 THEN 'Male'
        WHEN sex = 0 THEN 'Female'
        ELSE 'Unknown'
    END as gender,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM heart_disease), 2) as percentage,
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases
FROM heart_disease
GROUP BY sex
ORDER BY count DESC;

-- 6. Chest pain distribution
SELECT 
    CASE 
        WHEN cp = 1 THEN 'Typical Angina'
        WHEN cp = 2 THEN 'Atypical Angina'
        WHEN cp = 3 THEN 'Non-anginal Pain'
        WHEN cp = 4 THEN 'Asymptomatic'
        ELSE 'Unknown'
    END as chest_pain_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM heart_disease), 2) as percentage,
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases
FROM heart_disease
GROUP BY cp
ORDER BY count DESC;

-- 7. Maximum heart rate analysis
SELECT 
    ROUND(AVG(thalach), 2) as average_max_heart_rate,
    MIN(thalach) as min_max_heart_rate,
    MAX(thalach) as max_max_heart_rate,
    ROUND(STDDEV(thalach), 2) as std_dev_heart_rate
FROM heart_disease;

-- 8. Heart rate categories
SELECT 
    CASE 
        WHEN thalach < 120 THEN 'Low (<120)'
        WHEN thalach BETWEEN 120 AND 150 THEN 'Normal (120-150)'
        WHEN thalach BETWEEN 151 AND 180 THEN 'High (151-180)'
        ELSE 'Very High (>180)'
    END as heart_rate_category,
    COUNT(*) as count,
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases
FROM heart_disease
GROUP BY 
    CASE 
        WHEN thalach < 120 THEN 'Low (<120)'
        WHEN thalach BETWEEN 120 AND 150 THEN 'Normal (120-150)'
        WHEN thalach BETWEEN 151 AND 180 THEN 'High (151-180)'
        ELSE 'Very High (>180)'
    END
ORDER BY count DESC;

-- 9. High cholesterol patients (cholesterol > 240 mg/dl)
SELECT 
    COUNT(*) as total_patients,
    SUM(CASE WHEN chol > 240 THEN 1 ELSE 0 END) as high_cholesterol_patients,
    ROUND((SUM(CASE WHEN chol > 240 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) as high_cholesterol_percentage,
    SUM(CASE WHEN chol > 240 AND target = 1 THEN 1 ELSE 0 END) as high_cholesterol_with_heart_disease
FROM heart_disease;

-- 10. Blood pressure analysis
SELECT 
    ROUND(AVG(trestbps), 2) as average_blood_pressure,
    MIN(trestbps) as min_blood_pressure,
    MAX(trestbps) as max_blood_pressure,
    ROUND(STDDEV(trestbps), 2) as std_dev_blood_pressure
FROM heart_disease;

-- 11. Blood pressure categories
SELECT 
    CASE 
        WHEN trestbps < 120 THEN 'Normal (<120)'
        WHEN trestbps BETWEEN 120 AND 129 THEN 'Elevated (120-129)'
        WHEN trestbps BETWEEN 130 AND 139 THEN 'High Stage 1 (130-139)'
        WHEN trestbps BETWEEN 140 AND 179 THEN 'High Stage 2 (140-179)'
        ELSE 'Crisis (>180)'
    END as blood_pressure_category,
    COUNT(*) as count,
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases
FROM heart_disease
GROUP BY 
    CASE 
        WHEN trestbps < 120 THEN 'Normal (<120)'
        WHEN trestbps BETWEEN 120 AND 129 THEN 'Elevated (120-129)'
        WHEN trestbps BETWEEN 130 AND 139 THEN 'High Stage 1 (130-139)'
        WHEN trestbps BETWEEN 140 AND 179 THEN 'High Stage 2 (140-179)'
        ELSE 'Crisis (>180)'
    END
ORDER BY count DESC;

-- 12. Age group analysis
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
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases,
    ROUND((SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) as heart_disease_percentage
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
ORDER BY age_group;

-- 13. Risk factor correlation analysis
SELECT 
    'Age' as factor,
    ROUND(AVG(CASE WHEN target = 1 THEN age END), 2) as avg_with_disease,
    ROUND(AVG(CASE WHEN target = 0 THEN age END), 2) as avg_without_disease
FROM heart_disease
UNION ALL
SELECT 
    'Cholesterol' as factor,
    ROUND(AVG(CASE WHEN target = 1 THEN chol END), 2) as avg_with_disease,
    ROUND(AVG(CASE WHEN target = 0 THEN chol END), 2) as avg_without_disease
FROM heart_disease
UNION ALL
SELECT 
    'Blood Pressure' as factor,
    ROUND(AVG(CASE WHEN target = 1 THEN trestbps END), 2) as avg_with_disease,
    ROUND(AVG(CASE WHEN target = 0 THEN trestbps END), 2) as avg_without_disease
FROM heart_disease
UNION ALL
SELECT 
    'Max Heart Rate' as factor,
    ROUND(AVG(CASE WHEN target = 1 THEN thalach END), 2) as avg_with_disease,
    ROUND(AVG(CASE WHEN target = 0 THEN thalach END), 2) as avg_without_disease
FROM heart_disease;

-- 14. Exercise induced angina analysis
SELECT 
    CASE 
        WHEN exang = 1 THEN 'Yes'
        WHEN exang = 0 THEN 'No'
        ELSE 'Unknown'
    END as exercise_induced_angina,
    COUNT(*) as count,
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases,
    ROUND((SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) as heart_disease_percentage
FROM heart_disease
GROUP BY exang
ORDER BY count DESC;

-- 15. Fasting blood sugar analysis
SELECT 
    CASE 
        WHEN fbs = 1 THEN '> 120 mg/dl'
        WHEN fbs = 0 THEN '<= 120 mg/dl'
        ELSE 'Unknown'
    END as fasting_blood_sugar,
    COUNT(*) as count,
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as heart_disease_cases,
    ROUND((SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) as heart_disease_percentage
FROM heart_disease
GROUP BY fbs
ORDER BY count DESC;

-- 16. Comprehensive risk assessment
SELECT 
    age,
    sex,
    chol,
    trestbps,
    thalach,
    cp,
    thal,
    target,
    CASE 
        WHEN chol > 240 AND trestbps > 140 AND age > 55 THEN 'High Risk'
        WHEN chol > 200 OR trestbps > 130 OR age > 50 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as risk_level
FROM heart_disease
ORDER BY risk_level DESC, age DESC;
