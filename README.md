# AI-Based Student Placement Prediction and Skill Analysis System

## Overview
This end-to-end machine learning web application predicts whether a student is likely to get placed based on various factors (academic performance, technical skills, etc.). It also provides personalized skill recommendations and features an interactive dashboard.

## Project Structure
```
student-placement-ml/
│
├── data/
│   └── generate_data.py       # Script to generate synthetic dataset
│   └── student_placement.csv  # Generated dataset
│
├── models/
│   └── placement_model.pkl    # Trained ML model pipeline
│
├── src/
│   ├── preprocessing.py       # Data cleaning and feature engineering
│   ├── train.py               # Model training, evaluation, and saving
│   └── predict.py             # Inference logic
│
├── app.py                     # Streamlit frontend application
├── requirements.txt           # Dependencies
└── README.md
```

## Setup Instructions

1. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Dataset:**
   ```bash
   python data/generate_data.py
   ```

4. **Train Model:**
   ```bash
   python src/train.py
   ```

5. **Run Streamlit App:**
   ```bash
   streamlit run app.py
   ```
