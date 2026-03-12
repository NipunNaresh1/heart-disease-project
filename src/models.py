"""
Database models for the Heart Disease Analytics Dashboard.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HeartDisease(Base):
    """Heart disease patient data model."""
    
    __tablename__ = 'heart_disease'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False, comment='Age of the patient in years')
    sex = Column(Integer, nullable=False, comment='Sex (1 = male; 0 = female)')
    cp = Column(Integer, nullable=False, comment='Chest pain type (1-4)')
    trestbps = Column(Integer, nullable=False, comment='Resting blood pressure in mm Hg')
    chol = Column(Integer, nullable=False, comment='Serum cholesterol in mg/dl')
    fbs = Column(Integer, nullable=False, comment='Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)')
    restecg = Column(Integer, nullable=False, comment='Resting electrocardiographic results (0-2)')
    thalach = Column(Integer, nullable=False, comment='Maximum heart rate achieved')
    exang = Column(Integer, nullable=False, comment='Exercise induced angina (1 = yes; 0 = no)')
    oldpeak = Column(Float, nullable=False, comment='ST depression induced by exercise relative to rest')
    slope = Column(Integer, nullable=False, comment='The slope of the peak exercise ST segment (1-3)')
    ca = Column(Integer, nullable=False, comment='Number of major vessels (0-3) colored by fluoroscopy')
    thal = Column(Integer, nullable=False, comment='Thalassemia (1 = normal; 2 = fixed defect; 3 = reversible defect)')
    target = Column(Integer, nullable=False, comment='Heart disease (0 = no; 1 = yes)')
    created_at = Column(DateTime, default=datetime.utcnow, comment='Record creation timestamp')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='Record update timestamp')
    
    def __repr__(self):
        return f'<HeartDisease(id={self.id}, age={self.age}, target={self.target})>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'age': self.age,
            'sex': self.sex,
            'cp': self.cp,
            'trestbps': self.trestbps,
            'chol': self.chol,
            'fbs': self.fbs,
            'restecg': self.restecg,
            'thalach': self.thalach,
            'exang': self.exang,
            'oldpeak': self.oldpeak,
            'slope': self.slope,
            'ca': self.ca,
            'thal': self.thal,
            'target': self.target,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DataLog(Base):
    """Data processing and import logs."""
    
    __tablename__ = 'data_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(100), nullable=False, comment='Action performed (import, clean, etc.)')
    records_processed = Column(Integer, nullable=False, comment='Number of records processed')
    records_success = Column(Integer, nullable=False, comment='Number of successful records')
    records_failed = Column(Integer, default=0, comment='Number of failed records')
    error_message = Column(Text, comment='Error message if any')
    processing_time = Column(Float, comment='Processing time in seconds')
    created_at = Column(DateTime, default=datetime.utcnow, comment='Log creation timestamp')
    
    def __repr__(self):
        return f'<DataLog(id={self.id}, action={self.action}, records_processed={self.records_processed})>'
