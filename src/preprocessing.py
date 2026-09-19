import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MissingValueHandler(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.medians = {}

    def fit(self, X, y=None):
        for col in X.select_dtypes(include=[np.number]).columns:
            self.medians[col] = X[col].median()
        return self

    def transform(self, X):
        X_copy = X.copy()
        for col in X_copy.columns:
            if col in self.medians:
                X_copy[col] = X_copy[col].fillna(self.medians[col])
            elif X_copy[col].dtype == 'object':
                X_copy[col] = X_copy[col].fillna(X_copy[col].mode()[0])
        return X_copy

def preprocess_features(df):
    """
    Function to do initial cleanup like dropping ID columns.
    """
    df_clean = df.copy()
    if 'student_id' in df_clean.columns:
        df_clean = df_clean.drop('student_id', axis=1)
        
    df_clean = df_clean.drop_duplicates()
    return df_clean

def get_feature_columns():
    num_cols = [
        'cgpa', 'tenth_percentage', 'twelfth_percentage', 'aptitude_score', 
        'coding_score', 'technical_score', 'communication_score', 
        'number_of_projects', 'internship_months', 'certifications', 
        'attendance_percentage', 'backlogs'
    ]
    cat_cols = ['internship', 'extracurricular_activities']
    return num_cols, cat_cols
