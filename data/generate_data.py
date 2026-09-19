import pandas as pd
import numpy as np
import os

def generate_student_data(num_records=1500, save_path="data/student_placement.csv"):
    np.random.seed(42)

    # Base features
    cgpa = np.random.normal(loc=7.2, scale=1.1, size=num_records)
    cgpa = np.clip(cgpa, 4.0, 10.0)

    tenth_percentage = np.random.normal(loc=75, scale=12, size=num_records)
    tenth_percentage = np.clip(tenth_percentage, 45, 100)

    twelfth_percentage = tenth_percentage * 0.9 + np.random.normal(loc=5, scale=8, size=num_records)
    twelfth_percentage = np.clip(twelfth_percentage, 45, 100)

    aptitude_score = np.random.normal(loc=65, scale=15, size=num_records)
    aptitude_score = np.clip(aptitude_score, 10, 100)
    
    coding_score = cgpa * 8 + np.random.normal(loc=0, scale=15, size=num_records)
    coding_score = np.clip(coding_score, 10, 100)

    technical_score = coding_score * 0.7 + aptitude_score * 0.3 + np.random.normal(loc=0, scale=10, size=num_records)
    technical_score = np.clip(technical_score, 10, 100)
    
    communication_score = np.random.normal(loc=70, scale=18, size=num_records)
    communication_score = np.clip(communication_score, 20, 100)

    number_of_projects = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.1, 0.2, 0.35, 0.2, 0.1, 0.05], size=num_records)
    
    internship = np.random.choice(["Yes", "No"], p=[0.4, 0.6], size=num_records)
    internship_months = np.where(internship == "Yes", np.random.choice([1, 2, 3, 6], size=num_records), 0)
    
    certifications = np.random.choice([0, 1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.08, 0.02], size=num_records)
    
    attendance_percentage = np.random.normal(loc=82, scale=10, size=num_records)
    attendance_percentage = np.clip(attendance_percentage, 40, 100)
    
    backlogs = np.random.choice([0, 1, 2, 3, 4], p=[0.65, 0.15, 0.1, 0.05, 0.05], size=num_records)
    
    extracurricular_activities = np.random.choice(["Yes", "No"], p=[0.55, 0.45], size=num_records)

    # Target calculation logic (more realistic non-trivial threshold)
    # Give weights to create a composite score
    composite_score = (
        (cgpa / 10) * 0.25 + 
        (coding_score / 100) * 0.20 + 
        (technical_score / 100) * 0.15 + 
        (aptitude_score / 100) * 0.10 + 
        (communication_score / 100) * 0.10 +
        (number_of_projects / 5) * 0.10 +
        (internship_months / 6) * 0.05 + 
        (attendance_percentage / 100) * 0.05
    )
    
    # Penalize for backlogs
    composite_score -= backlogs * 0.03
    
    # Add noise to composite score
    composite_score += np.random.normal(0, 0.05, size=num_records)

    # Determine placement status based on composite score threshold (roughly 60% placed)
    threshold = np.percentile(composite_score, 40)
    placement_status = np.where(composite_score >= threshold, "Placed", "Not Placed")

    df = pd.DataFrame({
        'student_id': range(1, num_records + 1),
        'cgpa': np.round(cgpa, 2),
        'tenth_percentage': np.round(tenth_percentage, 2),
        'twelfth_percentage': np.round(twelfth_percentage, 2),
        'aptitude_score': np.round(aptitude_score, 2),
        'coding_score': np.round(coding_score, 2),
        'technical_score': np.round(technical_score, 2),
        'communication_score': np.round(communication_score, 2),
        'number_of_projects': number_of_projects,
        'internship': internship,
        'internship_months': internship_months,
        'certifications': certifications,
        'attendance_percentage': np.round(attendance_percentage, 2),
        'backlogs': backlogs,
        'extracurricular_activities': extracurricular_activities,
        'placement_status': placement_status
    })
    
    # Introduce a few random missing values for preprocessing practice (approx 2% missing in some columns)
    cols_with_missing = ['aptitude_score', 'communication_score', 'twelfth_percentage']
    for col in cols_with_missing:
        mask = np.random.rand(num_records) < 0.02
        df.loc[mask, col] = np.nan

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"Dataset generated successfully with {num_records} records at {save_path}")

if __name__ == '__main__':
    generate_student_data()
