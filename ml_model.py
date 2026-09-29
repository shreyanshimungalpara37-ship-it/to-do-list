from datetime import date
from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "priority_model.joblib"
CATEGORIES = ["Study", "Work", "Personal", "Health", "Finance", "Shopping"]
FEATURE_COLS = ["text", "category", "days_left", "duration_min", "importance", "overdue"]


def build_features(title, category, deadline, duration_min, importance, today=None):
    """Turn raw task input into the one-row DataFrame the model expects."""
    today = today or date.today()
    days_left = (deadline - today).days if deadline else 30
    return pd.DataFrame([{
        "text": title, "category": category, "days_left": days_left,
        "duration_min": duration_min, "importance": importance,
        "overdue": int(days_left < 0),
    }])[FEATURE_COLS]


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run: python model/train_model.py")
    return joblib.load(MODEL_PATH)


def predict_priority(title, category, deadline, duration_min, importance):
    model = load_model()
    X = build_features(title, category, deadline, duration_min, importance)
    return str(model.predict(X)[0])
