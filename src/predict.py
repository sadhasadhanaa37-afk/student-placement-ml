import joblib
import pandas as pd
import os
import json

MODEL_PATH = 'models/placement_model.pkl'

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None
    
def load_metrics():
    metrics_path = 'models/metrics.json'
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            return json.load(f)
    return None

def predict_placement(input_data):
    """
    Predicts the placement probability and class based on input features.
    input_data should be a dictionary containing the feature values.
    """
    model = load_model()
    if not model:
        raise FileNotFoundError("Model file not found. Please train the model first.")
        
    df_input = pd.DataFrame([input_data])
    
    # Prediction
    prediction = model.predict(df_input)[0]
    probability = model.predict_proba(df_input)[0][1]
    
    # Format the result
    result = {
        'prediction_class': 'Placed' if prediction == 1 else 'Not Placed',
        'probability': probability,
        'probability_percent': f"{probability * 100:.1f}%"
    }
    return result

def get_recommendations(input_data):
    """
    Generates actionable recommendations based on the input data.
    """
    recs = []
    
    if input_data.get('coding_score', 100) < 65:
        recs.append("Improve Python, problem solving, and Data Structures & Algorithms (DSA).")
        
    if input_data.get('aptitude_score', 100) < 65:
        recs.append("Practice quantitative aptitude, logical reasoning, and verbal ability.")
        
    if input_data.get('communication_score', 100) < 65:
        recs.append("Practice English communication, participate in Group Discussions, and do mock interviews.")
        
    if input_data.get('number_of_projects', 5) < 2:
        recs.append("Build 2-3 practical projects related to your domain to strengthen your resume.")
        
    if input_data.get('technical_score', 100) < 65:
        recs.append("Improve SQL, Python, ML fundamentals, and core computer science concepts.")
        
    if input_data.get('cgpa', 10.0) < 7.0:
        recs.append("Focus on improving your CGPA in the upcoming semesters. A score above 7.5 opens more opportunities.")
        
    if input_data.get('backlogs', 0) > 0:
        recs.append("Clear all pending backlogs as soon as possible. Many companies require zero active backlogs.")
        
    if not recs:
        recs.append("You have a strong profile! Keep practicing your interview skills and apply for mock interviews.")
        
    return recs
