# Tableau Visualization Plan for Heart Disease Analytics Dashboard

## Overview
This document outlines the comprehensive Tableau visualization strategy for the Heart Disease Analytics Project. The plan includes 8 core visualizations, an interactive dashboard, and a 5-scene story to communicate insights effectively.

## Dataset Column Descriptions

| Column | Description | Data Type |
|--------|-------------|-----------|
| age | Age of the patient in years | Integer |
| sex | Sex (1 = male; 0 = female) | Integer |
| cp | Chest pain type (1 = typical angina; 2 = atypical angina; 3 = non-anginal pain; 4 = asymptomatic) | Integer |
| trestbps | Resting blood pressure in mm Hg | Integer |
| chol | Serum cholesterol in mg/dl | Integer |
| fbs | Fasting blood sugar > 120 mg/dl (1 = true; 0 = false) | Integer |
| restecg | Resting electrocardiographic results (0 = normal; 1 = ST-T abnormality; 2 = LV hypertrophy) | Integer |
| thalach | Maximum heart rate achieved | Integer |
| exang | Exercise induced angina (1 = yes; 0 = no) | Integer |
| oldpeak | ST depression induced by exercise relative to rest | Float |
| slope | Peak exercise ST segment slope (1 = upsloping; 2 = flat; 3 = downsloping) | Integer |
| ca | Number of major vessels (0-3) colored by fluoroscopy | Integer |
| thal | Thalassemia (1 = normal; 2 = fixed defect; 3 = reversible defect) | Integer |
| target | Heart disease (0 = no; 1 = yes) | Integer |

## Data Preparation Steps

### 1. Data Cleaning
- Remove duplicate records
- Handle missing values (if any)
- Validate data ranges (age: 0-120, cholesterol: 100-400, etc.)

### 2. Data Transformation
- Convert numeric codes to meaningful labels:
  - sex: 0 → Female, 1 → Male
  - cp: 1 → Typical Angina, 2 → Atypical Angina, 3 → Non-anginal Pain, 4 → Asymptomatic
  - target: 0 → No Heart Disease, 1 → Heart Disease

### 3. Creating Calculated Fields

#### Age Group
```
IF [age] < 30 THEN "Under 30"
ELSEIF [age] < 40 THEN "30-39"
ELSEIF [age] < 50 THEN "40-49"
ELSEIF [age] < 60 THEN "50-59"
ELSEIF [age] < 70 THEN "60-69"
ELSE "70+"
END
```

#### Cholesterol Risk Level
```
IF [chol] < 200 THEN "Normal (<200)"
ELSEIF [chol] < 240 THEN "Borderline High (200-239)"
ELSE "High (>=240)"
END
```

#### Blood Pressure Category
```
IF [trestbps] < 120 THEN "Normal (<120)"
ELSEIF [trestbps] < 130 THEN "Elevated (120-129)"
ELSEIF [trestbps] < 140 THEN "High Stage 1 (130-139)"
ELSE "High Stage 2+ (>=140)"
END
```

#### Heart Rate Category
```
IF [thalach] < 120 THEN "Low (<120)"
ELSEIF [thalach] < 150 THEN "Normal (120-150)"
ELSEIF [thalach] < 180 THEN "High (151-180)"
ELSE "Very High (>180)"
END
```

#### High Cholesterol Risk
```
IF [chol] > 240 THEN "High Risk"
ELSE "Normal Risk"
END
```

#### Heart Rate Category
```
IF [thalach] < 100 THEN "Poor"
ELSEIF [thalach] < 120 THEN "Below Average"
ELSEIF [thalach] < 160 THEN "Average"
ELSE "Excellent"
END
```

## 8 Core Visualizations

### 1. Age Distribution (Bar Chart)
**Purpose**: Show the distribution of patients across age groups
- **Type**: Horizontal Bar Chart
- **Dimensions**: Age Group (calculated field)
- **Measures**: Count of patients, SUM of target
- **Color**: Use gradient from blue to red for heart disease prevalence
- **Tooltip**: Show percentage of heart disease in each age group

**Steps to Create**:
1. Drag "Age Group" to Columns
2. Drag "Number of Records" to Rows
3. Drag "target" to Color
4. Add percentage calculation to tooltip
5. Format with appropriate colors and labels

### 2. Gender Distribution (Pie Chart)
**Purpose**: Display gender breakdown and heart disease prevalence
- **Type**: Pie Chart
- **Dimensions**: Sex (converted to Male/Female)
- **Measures**: Count of patients
- **Color**: Blue for Male, Pink for Female
- **Additional**: Show heart disease cases as secondary measure

**Steps to Create**:
1. Create calculated field for gender labels
2. Drag "Sex" to Detail
3. Drag "Number of Records" to Angle
4. Drag "Sex" to Color
5. Add quick table calculation for percent of total

### 3. Cholesterol vs Heart Disease (Scatter Plot)
**Purpose**: Analyze relationship between cholesterol levels and heart disease
- **Type**: Scatter Plot
- **X-axis**: Age
- **Y-axis**: Cholesterol
- **Color**: Target (Heart Disease)
- **Size**: Number of Records
- **Shape**: Sex

**Steps to Create**:
1. Drag "Age" to Columns
2. Drag "chol" to Rows
3. Drag "target" to Color
4. Drag "sex" to Shape
5. Add trend line for correlation analysis

### 4. Chest Pain Type vs Heart Disease (Bar Chart)
**Purpose**: Show correlation between chest pain types and heart disease
- **Type**: Stacked Bar Chart
- **Dimensions**: Chest Pain Type (converted to labels)
- **Measures**: Count of patients
- **Color**: Target (Heart Disease)
- **Sorting**: By total count descending

**Steps to Create**:
1. Create calculated field for chest pain labels
2. Drag "Chest Pain Type" to Columns
3. Drag "Number of Records" to Rows
4. Drag "target" to Color
5. Add percentage calculations

### 5. Maximum Heart Rate Distribution (Histogram)
**Purpose**: Analyze distribution of maximum heart rates
- **Type**: Histogram
- **Measure**: Thalach (Maximum Heart Rate)
- **Bins**: Create bins of 10 BPM each
- **Color**: Target (Heart Disease)
- **Reference Lines**: Add average and median lines

**Steps to Create**:
1. Right-click "thalach" → Create → Bins
2. Drag "thalach (bin)" to Columns
3. Drag "Number of Records" to Rows
4. Drag "target" to Color
5. Add reference lines for statistics

### 6. Blood Pressure Trends (Line Chart)
**Purpose**: Show blood pressure patterns across age groups
- **Type**: Line Chart
- **X-axis**: Age
- **Y-axis**: Average Blood Pressure
- **Color**: Target (Heart Disease)
- **Trend Lines**: Add linear trend for each group

**Steps to Create**:
1. Drag "age" to Columns (convert to continuous)
2. Drag "trestbps" to Rows (set to Average)
3. Drag "target" to Color
4. Add trend lines
5. Format axes appropriately

### 7. Risk Factor Heatmap
**Purpose**: Visualize correlation between multiple risk factors
- **Type**: Heatmap
- **Rows**: Age Groups
- **Columns**: Cholesterol Risk Levels
- **Color**: Heart Disease Percentage
- **Size**: Number of Patients

**Steps to Create**:
1. Drag "Age Group" to Rows
2. Drag "Cholesterol Risk Level" to Columns
3. Drag "target" to Color (set to Average)
4. Drag "Number of Records" to Size
5. Format color palette from green to red

### 8. Age vs Cholesterol Relationship (Scatter Plot with Trend)
**Purpose**: Explore correlation between age and cholesterol
- **Type**: Scatter Plot
- **X-axis**: Age
- **Y-axis**: Cholesterol
- **Color**: Target
- **Trend Lines**: Separate for each target group
- **Quadrants**: Add average lines to create quadrants

**Steps to Create**:
1. Drag "Age" to Columns
2. Drag "chol" to Rows
3. Drag "target" to Color
4. Add reference lines for averages
5. Add trend lines for each color

## Interactive Dashboard Design

### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│                    TITLE & FILTERS                      │
├─────────────────────────────────────────────────────────┤
│  AGE DISTRIBUTION  │  GENDER DISTRIBUTION              │
│                     │                                   │
├─────────────────────┼───────────────────────────────────┤
│  CHEST PAIN VS      │  CHOLESTEROL VS HEART DISEASE     │
│  HEART DISEASE      │                                   │
├─────────────────────┼───────────────────────────────────┤
│  HEART RATE         │  BLOOD PRESSURE TRENDS            │
│  DISTRIBUTION       │                                   │
├─────────────────────┼───────────────────────────────────┤
│           RISK FACTOR HEATMAP                          │
└─────────────────────────────────────────────────────────┘
```

### Dashboard Filters
1. **Age Filter**: Range slider for age selection
2. **Gender Filter**: Single-select dropdown
3. **Cholesterol Filter**: Range slider for cholesterol levels
4. **Chest Pain Type Filter**: Multi-select dropdown
5. **Heart Disease Filter**: Yes/No toggle

### Actions and Interactions
- **Filter Actions**: Click on any chart to filter others
- **Highlight Actions**: Hover to highlight related data
- **URL Actions**: Click on data points to drill down to detailed views

## Tableau Story (5 Scenes)

### Scene 1 – Dataset Overview
**Title**: "Understanding Our Patient Population"
- **Content**: Total patient count, data quality metrics
- **Visualizations**: Summary statistics table, data completeness chart
- **Narrative**: Introduction to the dataset and its scope

### Scene 2 – Patient Demographics
**Title**: "Who Are Our Patients?"
- **Content**: Age distribution, gender breakdown, demographic insights
- **Visualizations**: Age distribution bar chart, gender pie chart
- **Narrative**: Analysis of patient demographics and their implications

### Scene 3 – Risk Factor Visualization
**Title**: "Identifying Key Risk Factors"
- **Content**: Cholesterol analysis, blood pressure trends, heart rate patterns
- **Visualizations**: Cholesterol scatter plot, BP line chart, heart rate histogram
- **Narrative**: Deep dive into physiological risk factors

### Scene 4 – Key Insights
**Title**: "What the Data Tells Us"
- **Content**: Correlation analysis, surprising findings, statistical significance
- **Visualizations**: Risk factor heatmap, correlation matrix
- **Narrative**: Highlight most important findings and their clinical relevance

### Scene 5 – Final Conclusion
**Title**: "Recommendations and Next Steps"
- **Content**: Summary of findings, clinical recommendations, future research directions
- **Visualizations**: Summary dashboard, key metrics comparison
- **Narrative**: Actionable insights and recommendations for healthcare providers

## Performance Optimization

### Dataset Size Considerations
- **Current Dataset**: 50+ records
- **Optimal Performance**: Up to 10,000 records for real-time interaction
- **Data Extracts**: Use Tableau extracts for improved performance
- **Aggregation**: Pre-aggregate data where possible

### Query Execution Performance
- **Calculated Fields**: Minimize complex calculations
- **Data Source Filters**: Apply filters at data source level
- **Context Filters**: Use context filters to improve performance
- **Fixed LODs**: Use FIXED LOD expressions for better performance

### Dashboard Loading Performance
- **Image Optimization**: Compress images and logos
- **Filter Optimization**: Use relevant filters only
- **Layout Optimization**: Minimize number of marks
- **Extract Refresh**: Schedule regular extract refreshes

## Best Practices

### Design Principles
- **Color Consistency**: Use consistent color scheme across all visualizations
- **Accessibility**: Ensure color-blind friendly palettes
- **Typography**: Use clear, readable fonts
- **White Space**: Maintain adequate spacing between elements

### Data Visualization Best Practices
- **Chart Selection**: Choose appropriate chart types for data
- **Labeling**: Clear and concise labels and titles
- **Tooltips**: Provide detailed information in tooltips
- **Interactivity**: Make dashboards interactive and user-friendly

### Storytelling Best Practices
- **Logical Flow**: Ensure scenes flow logically
- **Clear Narrative**: Each scene should tell part of the story
- **Visual Hierarchy**: Guide viewer attention to key insights
- **Concise Text**: Keep narrative text brief and impactful

## Implementation Timeline

### Phase 1: Data Preparation (1-2 days)
- Data cleaning and transformation
- Calculated field creation
- Data source connection setup

### Phase 2: Visualization Development (3-4 days)
- Create 8 core visualizations
- Test and refine each visualization
- Ensure consistency across charts

### Phase 3: Dashboard Assembly (2-3 days)
- Layout design and implementation
- Filter configuration
- Action setup and testing

### Phase 4: Story Creation (2 days)
- Develop 5-scene story
- Write narrative content
- Test story flow and transitions

### Phase 5: Testing and Refinement (1-2 days)
- Performance testing
- User acceptance testing
- Final refinements and deployment

This comprehensive plan ensures a professional, insightful, and interactive Tableau dashboard that effectively communicates heart disease analytics to healthcare professionals and stakeholders.
