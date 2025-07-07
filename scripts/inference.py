# scripts/inference.py
import os
import joblib

def model_fn(model_dir):
    """Load the model from the SageMaker model_dir"""
    return joblib.load(os.path.join(model_dir, "model.joblib"))
