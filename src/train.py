import os
import pandas as pd
import numpy as np
import joblib
import json
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from preprocessing import MissingValueHandler, preprocess_features, get_feature_columns

def train_and_evaluate():
    data_path = 'data/student_placement.csv'
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please run generate_data.py first.")
        return
        
    df = pd.read_csv(data_path)
    df = preprocess_features(df)
    
    # Split into features and target
    X = df.drop('placement_status', axis=1)
    y = df['placement_status'].map({'Placed': 1, 'Not Placed': 0})
    
    num_cols, cat_cols = get_feature_columns()
    
    # Create preprocessing pipeline
    numeric_transformer = Pipeline(steps=[
        ('imputer', MissingValueHandler()),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', MissingValueHandler()),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_cols),
            ('cat', categorical_transformer, cat_cols)
        ])
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Define models
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(),
        'Support Vector Machine': SVC(probability=True, random_state=42)
    }
    
    results = {}
    best_f1 = 0
    best_model_name = ""
    best_pipeline = None
    
    print("Training and evaluating models...")
    for name, model in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('classifier', model)])
                                   
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc = roc_auc_score(y_test, y_prob)
        
        results[name] = {
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-score': f1,
            'ROC-AUC': roc
        }
        
        print(f"--- {name} ---")
        print(f"Accuracy: {acc:.4f} | F1: {f1:.4f} | ROC-AUC: {roc:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = pipeline
            
    print(f"\nBest Model: {best_model_name} with F1-score: {best_f1:.4f}")
    
    # Optional: Hyperparameter tuning for the best model (e.g. Random Forest)
    if best_model_name == 'Random Forest':
        print("\nTuning Random Forest...")
        param_grid = {
            'classifier__n_estimators': [100, 200],
            'classifier__max_depth': [None, 10, 20],
            'classifier__min_samples_split': [2, 5]
        }
        
        grid_search = GridSearchCV(best_pipeline, param_grid, cv=5, scoring='f1', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        best_pipeline = grid_search.best_estimator_
        print("Tuning completed.")
        
        y_pred_tuned = best_pipeline.predict(X_test)
        best_f1 = f1_score(y_test, y_pred_tuned)
        print(f"Tuned F1-score: {best_f1:.4f}")
        
    # Evaluate final model on test set to get confusion matrix
    y_pred_final = best_pipeline.predict(X_test)
    cm = confusion_matrix(y_test, y_pred_final).tolist()
    
    final_metrics = {
        'model_name': best_model_name,
        'accuracy': accuracy_score(y_test, y_pred_final),
        'f1_score': best_f1,
        'confusion_matrix': cm
    }
    
    # Save the model and metrics
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_pipeline, 'models/placement_model.pkl')
    with open('models/metrics.json', 'w') as f:
        json.dump(final_metrics, f)
        
    print("Model and metrics saved successfully to 'models/' directory.")

if __name__ == '__main__':
    train_and_evaluate()
